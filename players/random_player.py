from board_util import board_print, calc_actions
from random import choice

class RandomPlayer:
    def __init__(self):
        pass

    def play(self, board):
        return choice(calc_actions(board))
