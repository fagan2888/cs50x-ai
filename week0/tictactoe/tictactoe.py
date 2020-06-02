"""
Tic Tac Toe Player
"""

import math
import copy
import random

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
    X_count = 0
    O_count = 0

    for row in board:
        for item in row:
            if item == X:
                X_count += 1
            if item == O:
                O_count += 1

    if X_count > O_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_set = set()

    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == EMPTY:
                action_set.add( (row, column) )
    
    return action_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid Action")
        

    board_copy = copy.deepcopy(board)
    
    i, j = action
    if player(board) == X:
        board_copy[i][j] = X
    else:
        board_copy[i][j] = O

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check the rows
    for row in board:
        player_type = row[0]
        player_count = 0
        for item in row:
            if item == player_type:
                player_count += 1
            else:
                break
        if player_count == 3:
            return player_type

    # Check the columns
    for column in range(3):
        player_type = board[0][column]
        player_count = 0
        for row in range(3):
            if board[row][column] == player_type:
                player_count += 1
            else:
                break
        if player_count == 3:
            return player_type

    # Check diagonals
    if board[0][0] == board[1][1] and board[0][0] == board[2][2]:
        return board[0][0]
    elif board[0][2] == board[1][1] and board[0][2] == board[2][0]:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O or len(actions(board)) == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    utility_temp = winner(board)
    if utility_temp == X:
        return 1
    elif utility_temp == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == True:
        return None

    # If empty / first move
    if board == [[EMPTY]*3]*3:
        return (random.randint(0,2), random.randint(0,2))

    # X = MAX, O = MIN
    current_player = player(board)
    action_list = actions(board)
    optimal_action = None

    if current_player == X:
        v = float("-inf")
        for action in action_list:
        #  MIN NOT MAX VALUE!!!
            temp = minValue(result(board, action))
            if temp > v:
                v = temp
                optimal_action = action

    if current_player == O:
        v = float("inf")
        for action in action_list:
            temp = maxValue(result(board, action))
            if temp < v:
                v = temp
                optimal_action = action

    return optimal_action


def maxValue(board):
    if terminal(board):
        return utility(board)

    v = float("-inf")
    for action in actions(board):
        v = max(v, minValue(result(board, action)))
    return v


def minValue(board):
    if terminal(board):
        return utility(board)

    v = float("inf")
    for action in actions(board):
        v = min(v, maxValue(result(board, action)))
    return v

