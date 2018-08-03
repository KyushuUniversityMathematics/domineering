#from board_util import board_print, can_put
from board_util import *
import numpy as np

class MonteCarloPlayer:
    def __init__(self, playout_num=100, max_depth=-1):
        self.playout_num = playout_num
        self.max_depth = max_depth

    def play(self, board): #
        return self.search_and_play(board, self.playout_num, self.max_depth)

    def search_and_play(self, board, playout_num, max_depth): #
        root_node = MTSNode(None, board, max_depth=max_depth) # start state
        for i in range(playout_num):
            node = root_node

            while len(node.actions) == 0 and len(node.children) > 0:
                node = node.select_node()

            if len(node.actions) > 0:
                node = node.expand_child()

            win = self.playout(node.board, node.turn) # playing one game
            node.backpropagate(win)
        action = root_node.select_action()
        return action

    def playout(self, board, turn):   #playing one game , return 1  - win, return -1 means lose
        board = np.copy(board)
        while True:
            actions = calc_actions(board)
            np.random.shuffle(actions)
            action = actions[0] if len(actions) > 0 else None
            if action is None:
                turn *= -1
                break
            board = calc_next_state(board, action)
            turn *= -1
        return turn

class MTSNode:
    def __init__(self, parent, board, turn=1, max_depth=-1, action=None):
        self.parent = parent
        self.board = board
        self.turn = turn
        self.action = action
        self.max_depth = max_depth
        
        self.children = []
        if max_depth == 0:
            self.actions = []
        else:
            self.actions = calc_actions(board)
            np.random.shuffle(self.actions)

        self.opponent_total_wins = 0
        self.total_playouts = 0

    def expand_child(self):
        action = self.actions.pop()
        board = calc_next_state(self.board, action)
        child = MTSNode(self, board, -self.turn, self.max_depth-1, action)
        self.children.append(child)
        return child

    def select_node(self):
        max_score = -float('inf')
        best_child = None
        for child in self.children:
            ucb = self.ucb(child)
            if max_score <= ucb:
                max_score = ucb
                best_child = child
        return best_child

    def select_action(self):  # retuns best action
        if len(self.children) == 0 and len(self.actions) == 0:
            return None
        best_child = None
        max_score = -float('inf')
        for child in self.children:
            score = child.opponent_total_wins / child.total_playouts # rate of wining game
            if score >= max_score:
                best_child = child
                max_score = score
        return best_child.action

    def ucb(self, child): # find good node for in playout
        c = 1
        return child.opponent_total_wins / child.total_playouts \
                + c * np.sqrt(np.log(self.total_playouts) / child.total_playouts)

    def backpropagate(self, win): # incrementing count of wining games
        node = self
        while not node is None:
            if node.turn == -win:
                node.opponent_total_wins += 1
            node.total_playouts += 1
            node = node.parent

    def get_root_node(self): # not use
        node = self
        while not node.parent is None:
            node = node.parent
        return node

    def print_route(self): # not use
        node = self
        while not node.parent is None:
            print(node.action, end='<-\n')
            node = node.parent
