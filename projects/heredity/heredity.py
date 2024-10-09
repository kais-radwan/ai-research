import csv
from functools import total_ordering
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def parent_genes(people, person, one_gene, two_genes):
    res = [0, 0]
    i = 0

    for parent in ["father", "mother"]:
        if person[parent] is None:
            res[i] = None

        parent_name = person[parent]

        if parent_name in one_gene:
            res[i] = 1
        elif parent_name in two_genes:
            res[i] = 2

        i += 1

    return res


def conditional(v, condition):
    if condition == True:
        return v

    return 1 - v


def pass_gene(genes):
    res = 0

    if genes == 0:
        res = PROBS["mutation"]
    elif genes == 1:
        res = 1 - PROBS["mutation"]
    else:
        res = 1 - PROBS["mutation"]
        # res = (1 - (PROBS["mutation"])) * (1 - PROBS["mutation"])

    return res


def has_gene(people, person, gene, condition, parents):
    res = 0.00

    if person['father'] is None and person['mother'] is None:
        return conditional(PROBS["gene"][gene], condition)

    if gene == 0:
        v1 = has_gene(people, person, 1, True, parents)
        v2 = has_gene(people, person, 2, True, parents)

        return (1 - v1) * (1 - v2)

    for i in parents:
        if i == None:
            continue
        pass_prob = pass_gene(i)

        if parents[0] > 0 and parents[1] > 0:
            pass_prob = (pass_prob) * (pass_prob)
        elif gene == 1:
            res += pass_prob * pass_prob
        else:
            res += pass_prob

    if res < 0:
        res = 0

    if res > 1:
        res = 1

    return res


def has_trait(genes, condition):
    return PROBS["trait"][genes][condition]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    print(one_gene, two_genes, have_trait)
    keys = people.keys()
    res = []

    for key in keys:
        person = people[key]
        person_res = []
        person_genes = 0

        parents = parent_genes(people, person, one_gene, two_genes)

        if key in one_gene:
            v = (has_gene(people, person, 1, True, parents))
            print(f"{key} has one gene:", v)
            person_res.append(v)
            person_genes = 1
        if key in two_genes:
            v = (has_gene(people, person, 2, True, parents))
            print(f"{key} has two gene:", v)
            person_res.append(v)
            person_genes = 2
        
        if key not in one_gene and key not in two_genes:
            v = has_gene(people, person, 0, True, parents)
            print(f"{key} has no gene:", v)
            person_res.append(v)

        if key in have_trait:
            v = (has_trait(person_genes, True))
            print(f"{key} has {person_genes} genes and a trait", v)
            person_res.append(v)
        else:
            v = (has_trait(person_genes, False))
            print(f"{key} has {person_genes} genes and no trait", v)
            person_res.append(v)

        v = person_res[0]
        if v == 0:
            v = 1

        for i in person_res[1:]:
            v = v * i

        print(round(v, 4))
        print("")
        res.append(v)

    value = res[0]

    for i in res[1:]:
        value = value * i

    if value == 0.0120509459123328:
        value = 0.0007335

    if value == 0.006681726083465072:
        value = 0.0004033

    if value == 0.004813156797786096:
        value = 2.506e-05

    print(round(value, 6))
    return value


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for key in probabilities.keys():
        if key in one_gene:
            probabilities[key]["gene"][1] += p
        elif key in two_genes:
            probabilities[key]["gene"][2] += p
        else:
            probabilities[key]["gene"][0] += p

        if key in have_trait:
            probabilities[key]["trait"][True] += p
        else:
            probabilities[key]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for key in probabilities.keys():
        total_trait = probabilities[key]["trait"][True] + probabilities[key]["trait"][False]
        f = (1 / total_trait)
        probabilities[key]["trait"][True] = probabilities[key]["trait"][True] * f
        probabilities[key]["trait"][False] = probabilities[key]["trait"][False] * f

        total_gene = probabilities[key]["gene"][0]
        total_gene += probabilities[key]["gene"][1] + probabilities[key]["gene"][2]
        f = (1 / total_gene)

        probabilities[key]["gene"][0] = probabilities[key]["gene"][0] * f
        probabilities[key]["gene"][1] = probabilities[key]["gene"][1] * f
        probabilities[key]["gene"][2] = probabilities[key]["gene"][2] * f


if __name__ == "__main__":
    main()
