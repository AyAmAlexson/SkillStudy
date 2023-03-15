import random


class Game:
    _board_user = None
    _board_cpu = None
    _winner = None
    _user_turn = None

    def __init__(self, gametype=10):
        self._board_user = Board(gametype)
        self._board_cpu = Board(gametype)
        self._user_turn = bool(random.getrandbits(1))

    def print_boards(self):
        tmp_board = self._board_user.status.copy()
        for i in range(len(tmp_board[0])):
            for j in range(len(tmp_board[i])):
                if j == 0:
                    tmp_board[i].append("\t\t\t" + str(self._board_cpu.status[i][j]))
                else:
                    tmp_board[i].append(str(self._board_cpu.status[i][j]))
        print(' |\n'.join(' | '.join(map(str, row)) for row in tmp_board), "|")
        tmp_board.clear()

    def game_play(self):
        while not self._winner:
            if self._user_turn:
                self.move_user()
                self.print_boards()
                self.check_winner()
                self._user_turn = not self._user_turn
            else:
                self.move_cpu()
                self.print_boards()
                self.check_winner()
                self._user_turn = not self._user_turn

        return self._winner

    def move_user(self):
        return True

    def move_cpu(self):
        return True

    def move_result(self):
        return True

    def check_winner(self):
        return True

    def ceremony(self):
        print('\n')
        if self._winner == 1:
            print("Поздравляем, Вы победили!")
        elif self._winner == 2:
            print("Сожалеем, Вы проиграли!")
        else:
            print("Что-то странное случилось, не знаю, кто победил")


class Board:
    _board = None

    def __init__(self, size=10):

        chars = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if size > len(chars) - 1:
            size = len(chars) - 1
        elif size < 2:
            size = 2
        self._board = [["O" for j in range(size + 1)] for i in range(size + 1)]
        for i in range(size + 1):
            self._board[i][0] = " " + str(i) if len(str(i)) < 2 else str(i)
            self._board[0][i] = chars[i] if i > 0 else "  "

    def print_board(self):
        print(' |\n'.join(' | '.join(map(str, row)) for row in self._board), "|")

    @property
    def status(self):
        return self._board


class Ship:
    x, y = None, None
    _horizontal = None
    _size = None

    def __init__(self, x, y, size, horizontal=True):
        self.x, self.y = x, y
        self._size = size
        self._horizontal = horizontal
