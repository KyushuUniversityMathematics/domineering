import numpy as np
from itertools import product

'''
board : ndarray with size n by n
action : tuple with 2 values whose format is (i, j) (0<=i<n-1, 0<=j<n)
'''

def create_board(n):
    return np.zeros((n, n))

def can_put(board, action):
    i, j = action
    n = len(board)
    return (0 <= i < n-1 and 0 <= j < n) and \
            np.all(1 - board[i:i+2, j])

def calc_actions(board):
    n = len(board)
    return [action for action in product(range(n), repeat=2) \
            if can_put(board, action)]

def calc_next_state(board, action):
    i, j = action
    next_state = np.copy(board)
    next_state[i:i+2, j] = 1
    return np.transpose(next_state)

def calc_next_states(board):
    return [calc_next_state(board, action) \
            for action in calc_actions(board)]

def is_finish(board):
    return np.all(board[:-1] + board[1:])

def board_to_str(board, trans=False):
    if trans:
        board = np.transpose(board)
    n = len(board)
    s = ''
    for i in range(n):
        for j in range(n):
            s += 'o' if board[i, j] else '.'
        s += '\n'
    return s

def board_print(board, trans=False):
    print(board_to_str(board, trans))

