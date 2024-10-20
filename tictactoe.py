"""
Tic Tac Toe Player
"""
from itertools import count
import random
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
    It always starts with X as first player
    """
    flattened_board = [cell for row in board for cell in row]

    if all(cell == EMPTY for cell in flattened_board) or flattened_board.count(X) == flattened_board.count(O):
        return X
    return O



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    available_actions = []
    for row_index, row in enumerate(board):
        for col_index, cell in enumerate(row):
            if cell == EMPTY:
                available_actions.append((row_index, col_index))
    random.shuffle(available_actions)
    return set(available_actions)

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    resulting_board = [row[:] for row in board]
    if not action:
        return board
    row, cell = action
    if resulting_board[row][cell] is not EMPTY:
        raise Exception("Action taken was already taken")
    resulting_board[row][cell] = player(board)
    return resulting_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    flattened_board = [cell for row in board for cell in row]
    is_game_over = terminal(board)
    if not is_game_over or (is_game_over and utility(board) == 0):
        return None
    if flattened_board.count(X) > flattened_board.count(O):
        return X
    return O



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    for i in range(3):
        # Check rows
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return True
        # Check columns
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return True

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return True
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return True

    # Check for a draw
    if all(cell != EMPTY for row in board for cell in row):
        return True

    # If we haven't returned yet, the game is not over
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        for i in range(3):
            if board[0][i] == board[1][i] == board[2][i] != EMPTY:
                return 1 if board[0][i] == X else -1
            if board[i][0] == board[i][1] == board[i][2] != EMPTY:
                return 1 if board[i][0] == X else -1
        if board[0][2] == board[1][1] == board[2][0] != EMPTY:
            return 1 if board[0][2] == X else -1
        if board[0][0] == board[1][1] == board[2][2] != EMPTY:
            return 1 if board[0][0] == X else -1
    return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)
    is_max = current_player == X
    best_move = None
    if is_max:
        best_score = -math.inf
    else:
        best_score = math.inf

    if terminal(board):
        return None

    for action in actions(board):
        board_result = result(board, action)
        opponent_move = minimax(board_result)
        score = utility(result(board_result, opponent_move))
        if is_max:
            if score > best_score:
                best_score = score
                best_move = action
        else:
            if score < best_score:
                best_score = score
                best_move = action
    return best_move
