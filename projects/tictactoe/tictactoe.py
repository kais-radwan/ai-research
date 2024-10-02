"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    xc = 0
    oc = 0

    for r in board:
        for i in r:
            if i == X:
                xc += 1
            elif i == O:
                oc += 1

    if xc > oc:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    for i in range(3):
        row = board[i]
        for t in range(3):
            if row[t] == EMPTY:
                actions.add((i, t))

    for ac in actions:
        if board[ac[0]][ac[1]] != EMPTY:
            actions.remove(ac)

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2:
        raise Exception("Invalid Action")

    if board[action[0]][action[1]] in [X, O]:
        raise Exception("Move already taken")

    try:
        new_board = [row[:] for row in board]
        new_board[action[0]][action[1]] = player(board)
        return new_board
    except:
        raise Exception("Unexpected error")

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        row = board[i]
        if all(c == X for c in row):
            return X
        elif all(c == O for c in row):
            return O

    for i in range(3):
        col = [board[0][i], board[1][i], board[2][i]]
        if all(c == X for c in col):
            return X
        elif all(c == O for c in col):
            return O

    cross_1 = [board[0][0], board[1][1], board[2][2]]
    cross_2 = [board[0][2], board[1][1], board[2][0]]

    if all(c == X for c in cross_1):
        return X
    elif all(c == O for c in cross_1):
        return O
    elif all(c == X for c in cross_2):
        return X
    elif all(c == O for c in cross_2):
        return O

    # default return
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    game_winner = winner(board=board)
    if game_winner is not None:
        return True

    available_actions = actions(board=board)
    if len(available_actions) == 0:
        return True

    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board=board)

    if game_winner == X:
        return 1
    
    if game_winner == O:
        return -1
    
    return 0

def min_value(board):
    if terminal(board):
        return utility(board)

    value = math.inf
    for action in actions(board):
        try:
            value = min(value, max_value(result(board, action)))
        except:
            pass

    return value

def max_value(board):
    if terminal(board=board):
        return utility(board=board)

    value = -math.inf
    for action in actions(board):
        try:
            value = max(value, min_value(result(board, action)))
        except:
            pass

    return value

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    available_actions = actions(board=board)

    if len(available_actions) == 9:
        return available_actions[0]

    if player(board) == X:
        value = -math.inf
        best_action = None
        for action in available_actions:
            new_value = min_value(board=result(board, action))
            if new_value > value:
                value = new_value
                best_action = action

        return best_action
    else:
        value = math.inf
        best_action = None
        for action in available_actions:
            new_value = max_value(board=result(board, action))
            if new_value < value:
                value = new_value
                best_action = action
        return best_action