from board_util import (create_board, is_finish,
        calc_next_state, board_print)
import sys
from tqdm import tqdm

from human_player import HumanPlayer

def play_game(n, player1, player2, names=None, output=True):
    if not names:
        names = ['player1', 'player2']
    board = create_board(n)
    turn = 0
    players = [player1, player2]
    while not is_finish(board):
        action = players[turn].play(board)
        board = calc_next_state(board, action)
        turn ^= 1
    try:
        player1.finish()
    except:
        pass
    try:
        player2.finish()
    except:
        pass
    human = None
    for i, player in enumerate(players):
        if isinstance(player, HumanPlayer):
            human = i
    if human is not None:
        print('final result')
        board_print(board, human^turn)

    winner = turn^1
    if output:
        print('{} win!'.format(names[winner]))
    return winner

def play_games(n, player1, player2, times=100, show=False):
    names = ['player1', 'player2']
    win_num = [0, 0]
    ite = range(times)
    if not show:
        ite = tqdm(ite)
    for i in ite: 
        winner = play_game(n, player1, player2, output=False)
        win_num[winner] += 1
        if show:
            print('{}-1: {} win'.format(i, names[winner]))
        winner = play_game(n, player2, player1, output=False)
        if show:
            print('{}-2: {} win'.format(i, names[winner^1]))
        win_num[winner^1] += 1
    print('first: {}, second: {}'.format(win_num[0], win_num[1]))
    return win_num

#if __name__ == '__main__':
#    play_games(4, DQNPlayer(4), RandomPlayer())
 #   exit()
#    game_num = 1 if len(sys.argv) < 2 else int(sys.argv[1])
 #   n = 4

#    for i in range(game_num):
#        print('{} th game'.format(i))
 #       play_game(n, HumanPlayer(), DQNPlayer(n))
