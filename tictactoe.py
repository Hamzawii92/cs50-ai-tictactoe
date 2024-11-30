"""
Tic Tac Toe Player
"""

import math
import copy

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
    Returns player who has next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    
    return O if x_count > o_count else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move at (i, j).
    """
    if action not in actions(board):
        raise Exception("Invalid action")
    
    # Create a deep copy of the board
    new_board = copy.deepcopy(board)
    i, j = action
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in board:
        if row.count(row[0]) == len(row) and row[0] is not EMPTY:
            return row[0]
    
    # Check columns
    for j in range(3):
        column = [board[i][j] for i in range(3)]
        if column.count(column[0]) == len(column) and column[0] is not EMPTY:
            return column[0]
    
    # Check diagonals
    diag1 = [board[i][i] for i in range(3)]
    diag2 = [board[i][2-i] for i in range(3)]
    
    if diag1.count(diag1[0]) == len(diag1) and diag1[0] is not EMPTY:
        return diag1[0]
    
    if diag2.count(diag2[0]) == len(diag2) and diag2[0] is not EMPTY:
        return diag2[0]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(EMPTY not in row for row in board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)
    if game_winner == X:
        return 1
    elif game_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    current_player = player(board)
    
    if current_player == X:
        # Maximizing player
        v = float('-inf')
        best_move = None
        for action in actions(board):
            min_val = min_value(result(board, action))
            if min_val > v:
                v = min_val
                best_move = action
        return best_move
    
    else:
        # Minimizing player
        v = float('inf')
        best_move = None
        for action in actions(board):
            max_val = max_value(result(board, action))
            if max_val < v:
                v = max_val
                best_move = action
        return best_move


def max_value(board):
    """
    Returns the maximum value for the board state.
    """
    if terminal(board):
        return utility(board)
    
    v = float('-inf')
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    """
    Returns the minimum value for the board state.
    """
    if terminal(board):
        return utility(board)
    
    v = float('inf')
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
