import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        variables = self.domains.keys()

        for var in variables:
            domains = set(self.domains[var])
            for dom in domains:
                if len(dom) != var.length:
                    self.domains[var].remove(dom)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        changed = False

        if (x, y) not in self.crossword.overlaps:
            return False

        overlaps = self.crossword.overlaps[x, y]
        x_domains = set(self.domains[x])
        y_domains = set(self.domains[y])

        if overlaps is None:
            return False

        for dom in x_domains:
            passes = False
            x_char = dom[overlaps[0]]

            for ydom in y_domains:
                y_char = ydom[overlaps[1]]

                if x_char == y_char:
                    passes = True

            if passes == False:
                changed = True
                self.domains[x].remove(dom)

        return changed

    def all_arcs(self):
        arcs = []
        keys = list(self.domains.keys())

        for var in keys:
            for var2 in keys:
                if (var, var2) not in self.crossword.overlaps.keys():
                    continue

                over = self.crossword.overlaps[var, var2]

                if over is not None:
                    arcs.append((var, var2))

        return arcs

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = self.all_arcs()

        while len(arcs) > 0:
            (x, y) = arcs.pop(0)
            changed = self.revise(x, y)

            if changed == False:
                continue

            if len(self.domains[x]) == 0:
                return False

            neighbors = self.crossword.neighbors(x)
            for n in neighbors:
                if n == y:
                    continue

                arcs.append((n, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        keys = list(assignment.keys())

        for var in self.crossword.variables:
            if var in keys and assignment[var] is not None:
                continue

            return False

        return True

    def right_value(self, var, value):
        if len(value) != var.length:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        keys = list(assignment.keys())

        for var in keys:
            value = assignment[var]

            for var2 in keys:
                if var2 == var:
                    continue

                if value == assignment[var2]:
                    return False

            passes = self.right_value(var, value)
            if passes == False:
                return False

            neighbors = self.crossword.neighbors(var)

            if len(neighbors) < 1:
                continue

            for n in neighbors:
                if n not in keys:
                    continue

                nvalue = assignment[n]
                cross = self.crossword.overlaps[var, n]
                if value[cross[0]] != nvalue[cross[1]]:
                    return False

        return True

    def rollout(self, var, value, pos):
        n = 0

        for v in self.domains[var]:
            if value[pos[0]] != v[pos[1]]:
                n += 1

        return n

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        keys = list(assignment.keys())
        res = {}
        ordered_values = []

        for value in self.domains[var]:
            neighbors = self.crossword.neighbors(var)
            added = False

            for n in neighbors:
                if n in keys:
                    continue

                if (var, n) not in self.crossword.overlaps.keys():
                    continue

                overlap = self.crossword.overlaps[var, n]
                out = self.rollout(n, value, overlap)

                if value in res.keys():
                    res[value] += out
                else:
                    res[value] = out

                added = True

            if value not in res.keys():
                res[value] = 0

        res_keys = list(res.keys())

        if len(res_keys) < 1:
            return []

        max_res = max(res.values())
        i = 0

        while i <= max_res:
            for key in res_keys:
                if res[key] == i:
                    ordered_values.append(key)

            i += 1

        return ordered_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        assignment_keys = assignment.keys()

        best_var = None
        vars = {}
        mini_vars = {}

        minimum_value = float('inf')
        highest_degree = float('-inf')

        def add_value(d, k, v):
            if k in d.keys():
                d[k].append(v)
            else:
                d[k] = [v]

        for var in list(self.crossword.variables):
            if var in assignment_keys:
                continue

            remain = len(self.domains[var])

            if remain < minimum_value:
                add_value(mini_vars, remain, var)
                minimum_value = remain

            degrees = len(self.crossword.neighbors(var))
            vars[var] = (remain, degrees)

        mini = mini_vars[minimum_value]
        if len(mini) == 1:
            return mini[0]

        for var in mini:
            if best_var is None:
                best_var = var
                highest_degree = vars[var][1]
                continue

            if vars[var][1] > highest_degree:
                highest_degree = vars[var][1]
                best_var = var

        return best_var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        vars = self.crossword.variables

        if len(vars) == len(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        domains = self.order_domain_values(var, assignment)

        for value in domains:
            new_a = dict(assignment.copy())
            new_a[var] = value

            if self.consistent(new_a) == False:
                continue

            res = self.backtrack(new_a)
            if res is not None:
                return res

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
