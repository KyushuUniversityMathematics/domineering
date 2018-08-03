from board_util import board_print, can_put

class HumanPlayer:
    def __init__(self):
        pass

    def play(self, board):
        board_print(board)
        while True:
            try:
                i, j = map(int, input('input position: ').split())
                if can_put(board, (i, j)):
                    return i, j
                print('can not put there')
            except ValueError:
                print('input is not correct')
            except KeyboardInterrupt:
                print('killing process ...')
                exit()


