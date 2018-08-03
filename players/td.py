import random
import numpy as np
from board_util import *
from td_network import create_td_model
from game import play_games
from game import play_game
from random_player import RandomPlayer
from monte_carlo_player import MonteCarloPlayer

EPISODES = 10000

class TDAgent:
    def __init__(self, n, gamma=0.95, epsilon=1.0):
        self.n = n
        self.gamma = gamma
        self.epsilon = epsilon
        self.model = self._build_model()

    def _build_model(self):
        return create_td_model(self.n)

    def act(self, state, epsilon=None, learn=False):
        if epsilon is None:
            epsilon = self.epsilon

        actions = calc_actions(state)
        if np.random.rand() <= epsilon:
            best_action = random.choice(actions)
            best_value = None
        else:
            next_states = calc_next_states(state)
            #rewards = np.array([float(is_finish(board)) for board in next_states])
            next_states = np.array(next_states)
            values = -self.model.predict(next_states).ravel()
            best_index = np.argmax(values)
            best_action = actions[best_index]
            best_value = values[best_index]

        next_state = calc_next_state(state, best_action)
        target = None
        if is_finish(next_state):
            target = 1
        elif best_value is not None:
            target = self.gamma * best_value

        if learn and target is not None:
            self.model.fit(state[np.newaxis,:,:],
                    np.array([[target]]), verbose=0, epochs=1)
        return best_action

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


from board_util import board_print, calc_actions, can_put
from network_creator import create_model

class TDPlayer:
    def __init__(self, n, filename='td_weight.h5', agent=None):
        if agent is None:
            self.agent = TDAgent(n)
            self.agent.load(filename)
        else:
            self.agent = agent


    def play(self, board):
        action = self.agent.act(board, epsilon=0.0)
        #print(action)
        assert can_put(board, action)
        return action



if __name__ == '__main__':
    n = 4
    agent = TDAgent(n, epsilon=0.1)

    t123 = 2
    savefile = open('win_rate_of_td.txt', mode='w')
    count1 = []
    done = False
    for e in range(EPISODES):
        state = create_board(n)
        while True:
            action = agent.act(state, learn=True)
            state = calc_next_state(state, action)
            done = is_finish(state)
            if done:
                print('episode: {}/{}, e: {:.2}'
                        .format(e, EPISODES, agent.epsilon))
                break
        if e % t123 == 0:
            for i in range(20):
                players = play_game(n, TDPlayer(n=n, filename=None, agent=agent), MonteCarloPlayer())
                count1.append(players)
                # print('winrate is {}'.format(count1.count(0)/len(count1)))
            savefile.write('{},'.format(count1.count(0) / len(count1)))

            # win, lose = play_games(n, TDPlayer(n=n, filename=None, agent=agent), MonteCarloPlayer(), times=50)
            # print('winrate is {}'.format(win / (win + lose)))
            # savefile.write('{},'.format(win / (win + lose)))
        if e == EPISODES-1:
            agent.save('td_weight.h5')
