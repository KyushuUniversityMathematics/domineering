from board_util import board_print, calc_actions, can_put
from network_creator import create_model
from td import TDAgent

class TDPlayer:
    def __init__(self, n, filename='td_weight.h5'):
        self.agent = TDAgent(n)
        self.agent.load(filename)

    def play(self, board):
        action = self.agent.act(board, epsilon=0.0)
        #print(action)
        assert can_put(board, action)
        return action
