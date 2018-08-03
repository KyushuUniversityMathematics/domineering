from human_player import HumanPlayer
from random_player import RandomPlayer
from dqn import DQNPlayer
from td_player import TDPlayer
from game import *
from monte_carlo_player import MonteCarloPlayer

#play_games(8, RandomPlayer(), MonteCarloPlayer(), times=100, show=True)
with open('q_value_of_td.txt','w') as f:
	play_games(4, TDPlayer(4, savefile = f), RandomPlayer(), times=100, show=True)
#play_games(4, HumanPlayer(), MonteCarloPlayer(), times=1, show=True)
#play_games(8, TDPlayer(8), MonteCarloPlayer(), times=2, show=True)
#play_games(4, DQNPlayer(4), TDPlayer(4), times=100, show=True)