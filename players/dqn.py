import random
import numpy as np
from collections import deque

from network_creator import create_model
from board_util import *
from game import play_games
from game import play_game
from random_player import RandomPlayer
from monte_carlo_player import MonteCarloPlayer


EPISODES = 10000

class DQNAgent:
    def __init__(self, n, gamma=0.95, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995, learning_rate=0.001):
        self.n = n
        self.memory = deque(maxlen=2000)
        self.gamma = gamma
        '''
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        '''
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate
        self.model = self._build_model()

    def _build_model(self):
        return create_model(self.n, self.learning_rate)

    def remember(self, state, next_state, reward, done):
        self.memory.append((state, next_state, reward, done))

    def act(self, state, epsilon=None, remember=False):
        if epsilon is None:
            epsilon = self.epsilon

        actions = calc_actions(state)
        if np.random.rand() <= epsilon:
            best_action = random.choice(actions)
            best_value = None
        else:
            next_states = calc_next_states(state)
            best_action = None
            best_value = -float('inf')
            for action, next_state in zip(actions, next_states):
                act_value = self.model.predict(
                        [state[np.newaxis,:,:],
                            next_state[np.newaxis,:,:]])[0,0]
                #print(act_value)
                if act_value > best_value:
                    best_value = act_value
                    best_action = action
            #print(actions)
            #print(actions.index(best_action))
        if remember:
            next_state = calc_next_state(state, best_action)
            done = is_finish(next_state)
            reward = 1 if done else 0
            self.remember(state, next_state, reward, done)
            if done:
                for _ in range(20):
                    self.remember(state, next_state, reward, done)
        return best_action, best_value

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, next_state, reward, done in minibatch:
            target = reward
            if not done:
                _, best_value = self.act(next_state, epsilon=0.0)
                target = reward - self.gamma * best_value



            self.model.fit([state[np.newaxis,:,:],
                next_state[np.newaxis,:,:]],
                np.array([[target]]), verbose=0,
                epochs=1)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

class DQNPlayer:
    def __init__(self, n, filename='dqn_weight.h5', agent=None, savefile=None):
        if filename is None and agent is not None:
            self.agent = agent
        else:
            self.agent = DQNAgent(n)
            self.agent.load(filename)
        self.savefile = savefile

    def play(self, board):
        action, q_value = self.agent.act(board, epsilon=0.0)
        #print(action)
        assert can_put(board, action)
        if self.savefile is not None:
            self.savefile.write('{},'.format(q_value))
        return action
    
    def finish(self):
        if self.savefile is not None:
            self.savefile.write('\n')
    
if __name__ == '__main__':
    n = 4
    agent = DQNAgent(n, epsilon_min=0.1)

    done = False
    batch_size = 128
    
    t123 = 2
    savefile = open('win_rate_of_dqn_r_128_2000.txt', mode='w')
    count1 = []

    for e in range(EPISODES):
        state = create_board(n)
        while True:
            action, _ = agent.act(state, remember=True)
            state = calc_next_state(state, action)
            done = is_finish(state)
            if done:
                print('episode: {}/{}, e: {:.2}'
                        .format(e, EPISODES, agent.epsilon))
                break
        if len(agent.memory) > batch_size:
            agent.replay(batch_size)
        if e % t123 == 0:
            for i in range(20):

                players = play_game(n, DQNPlayer(n=n, filename=None, agent=agent),RandomPlayer())
                count1.append(players)
                # print('winrate is {}'.format(count1.count(0)/len(count1)))
            savefile.write('{},'.format(count1.count(0)/len(count1)))
                #savefile.write('{},'.format(count1.count(1) / len(count1)))

        # if e % t123 == 0:
        #     win, lose = play_games(n, DQNPlayer(n=n, filename=None, agent=agent), MonteCarloPlayer(), times=1)
        #     print('winrate is {}'.format(win/(win+lose)))
        #     savefile.write('{},'.format(win/(win+lose)))
        if e == EPISODES-1:
            agent.save('dqn_weight.h5')
            savefile.close()

