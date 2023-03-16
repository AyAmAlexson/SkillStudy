import random as r
from ShipsDistribution import SHIPS_DISTR


class Ship:               # Класс корабля
    x, y = None, None     # Координаты на доске
    _horizontal = None    # Ориентация (вертикально/горизонтально)
    _size = None          # Размер корабля
    _body = None          # Корпус корабля - список клеток. при пробитии одной из клеток соответствующий символ корпуса будет изменяться

    def __init__(self, size):
        self._size = size
        self._body = ["◼" for i in range(size)]

    @property
    def get_body(self):
        return self._body

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_orientation(self, hor):
        self._horizontal = hor

    @property
    def get_orientation(self):
        return self._horizontal

    @property
    def get_x_position(self):
        return self.x

    @property
    def get_y_position(self):
        return self.y

    @property
    def get_size(self):
        return self._size


class Game:                     # Класс игры
    _board_user = None          # Поле игрока
    _board_cpu = None           # Поле компьютера
    _winner = None              # Победитель, при проверке на победителя будет присваиваться значение 1, если победил игрок, и 2, если победил компьютер
    _user_turn = None           # Очередность хода
    _game_size = None           # Размер поля
    _user_ships = None          # Набор кораблей игрока
    _cpu_ships = None           # Набор кораблей компьютера

    def __init__(self, game_type=10):
        if game_type > 26:
            game_type = 26
        elif game_type < 2:
            game_type = 2
        self._board_user = Board(game_type)
        self._board_cpu = Board(game_type)
        self._user_turn = bool(r.getrandbits(1))  # Пока первый ход определяется рандомно
        self._game_size = game_type

    def generate_ships_user(self):
        self._user_ships = []
        for ship_size in SHIPS_DISTR[self._game_size]:   # Набор кораблей для этого размера поля забираем из константы в файле ShipsDistribution
            new_ship = Ship(ship_size)                   # Создаем объекты класса Корабль разного размера
            self._user_ships.append(new_ship)            # Добавляем в список кораблей игрока

    def generate_ships_cpu(self):                        # Аналогично создадим список кораблей компьютера
        self._cpu_ships = []
        for ship_size in SHIPS_DISTR[self._game_size]:
            new_ship = Ship(ship_size)
            self._cpu_ships.append(new_ship)

    def print_boards(self):                                 # Метод вывода на экран сразу двух полей
        tmp_board = self._board_user.status.copy()
        print("\n",
              " " * int(len(tmp_board[0]) * 1.5), "ТВОЕ ПОЛЕ",
              " " * int(len(tmp_board[0]) * 1.5), "\t\t" * (len(tmp_board[0]) // 3), "ПОЛЕ ПРОТИВНИКА",
              " " * int(len(tmp_board[0]) * 1.5), "\n")

        for i in range(len(tmp_board[0])):
            for j in range(len(tmp_board[i])):
                if j == 0:
                    tmp_board[i].append("\t\t\t" + str(self._board_cpu.status[i][j]))
                else:
                    tmp_board[i].append(str(self._board_cpu.status[i][j]))
        print(' |\n'.join(' | '.join(map(str, row)) for row in tmp_board), "|")
        tmp_board.clear()

    def random_placement_user(self):                        # Метод для рандомной расстановки кораблей пользователя
        while True:                                         # Иногда возникают такие ситуации, когда не выходит расставить все корабли по правилам, тк не хватает места.
            for ship in self._user_ships[::-1]:             # Поэтому я сделал так, чтобы если после 100 попыток не получается расставить корабли, обнуляем доску и начинаем сначала
                ok = False
                iter=0
                while not ok:
                    iter += 1
                    if iter == 100:
                        break
                    ship.set_position(r.randint(1, self._game_size), r.randint(1, self._game_size))   # Ставим корабль в рандомное место
                    ship.set_orientation(bool(r.getrandbits(1)))
                    try:
                        self.check_vs_board(ship, self._board_user)                                   # Проверяем, можно ли его туда поставить
                    except Exception:
                        pass                                                                          # Если ловится выброшенная нами ошибка, то повторяем для следующего рандомного места
                    else:
                        ok = True
                        self.put_the_ship_on_the_board_user(ship)                                     # Если получилось поставить, то наносим его на доску и переходим к следующему кораблю
            if ok:
                return True
            self._board_user.reset(self._game_size)



    def random_placement_cpu(self):                         # Aналогично расстанавливаем корабли компьюетера
        while True:
            for ship in self._cpu_ships[::-1]:
                ok = False
                iter = 0
                while not ok:
                    iter += 1
                    if iter == 100:
                        break
                    ship.set_position(r.randint(1, self._game_size), r.randint(1, self._game_size))
                    ship.set_orientation(bool(r.getrandbits(1)))
                    try:
                        self.check_vs_board(ship, self._board_cpu)
                    except Exception:
                        pass
                    else:
                        ok = True
                        self.put_the_ship_on_the_board_cpu(ship)
            if ok:
                return True
            self._board_cpu.reset(self._game_size)


    @staticmethod
    def check_vs_board(ship: Ship, board):                  # Статический метод проверки на возможность поставить корабль с такими координатами
        ok = False
        x = ship.get_x_position
        y = ship.get_y_position

        if ship.get_orientation:
            for i in range(ship.get_size):
                if board.status[x+i][y] == "◼":
                    raise ValueError("Can't put the tile here")
                check_the_board_around_tile(x + i - 1, y - 1, board)
                check_the_board_around_tile(x + i - 1, y, board)
                check_the_board_around_tile(x + i - 1, y + 1, board)
                check_the_board_around_tile(x + i , y - 1, board)
                check_the_board_around_tile(x + i , y + 1, board)
                check_the_board_around_tile(x + i + 1, y, board)
                check_the_board_around_tile(x + i + 1, y - 1, board)
                check_the_board_around_tile(x + i + 1, y + 1, board)
        else:
            for i in range(ship.get_size):
                if board.status[x][y+i] == "◼":
                    raise ValueError("Can't put the tile here")

                check_the_board_around_tile(x - 1, y + i - 1, board)
                check_the_board_around_tile(x - 1, y + i, board)
                check_the_board_around_tile(x - 1, y + i + 1, board)
                check_the_board_around_tile(x, y + i - 1, board)
                check_the_board_around_tile(x, y + i + 1, board)
                check_the_board_around_tile(x + 1, y + i, board)
                check_the_board_around_tile(x + 1, y + i - 1, board)
                check_the_board_around_tile(x + 1, y + i + 1, board)

    def put_the_ship_on_the_board_user(self, ship:Ship):
        x = ship.get_x_position
        y = ship.get_y_position
        if ship.get_orientation:
            for i in range(ship.get_size):
                self._board_user.set_tile(x+i,y,"◼")
        else:
            for i in range(ship.get_size):
                self._board_user.set_tile(x,y+i,"◼")

    def put_the_ship_on_the_board_cpu(self, ship:Ship):
        x = ship.get_x_position
        y = ship.get_y_position
        if ship.get_orientation:
            for i in range(ship.get_size):
                self._board_cpu.set_tile(x+i,y,"◼")
        else:
            for i in range(ship.get_size):
                self._board_cpu.set_tile(x,y+i,"◼")


    def game_play(self):
        self.generate_ships_user()
        self.random_placement_user()
        self.generate_ships_cpu()
        self.random_placement_cpu()
        self.print_boards()

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


def check_the_board_around_tile(x,y,board):
    try:
        if board.status[x][y] == "◼":
            raise ValueError("Can't put the tile here")
    except IndexError:
        pass


class Board:
    _board = None

    def __init__(self, size=10):

        chars = " 🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩"
        if size > len(chars) - 1:
            size = len(chars) - 1
        elif size < 2:
            size = 2
        self._board = [["☐" for j in range(size + 1)] for i in range(size + 1)]   #◈
        for i in range(size + 1):
            self._board[i][0] = " " + str(i) if len(str(i)) < 2 else str(i)
            self._board[0][i] = chars[i] if i > 0 else "  "

    def reset(self, size):
        for i in range(1,size+1):
            for j in range(1,size+1):
                self._board[i][j] = "☐"



    def print_board(self):
        print(' |\n'.join(' | '.join(map(str, row)) for row in self._board), "|")

    @property
    def status(self):
        return self._board

    def set_tile(self,x,y, value):
        self._board[x][y] = value