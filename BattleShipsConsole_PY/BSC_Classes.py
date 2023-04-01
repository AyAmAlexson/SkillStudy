import random as r
import time
from ShipsDistribution import SHIPS_DISTR


class Player:
    _ship_set = None
    _AI_mode = None
    _my_board = None
    _vs_board = None

    def __init__(self, mode: bool, game_size):
        self._AI_mode = mode
        self._my_board = Board(game_size)
        self._vs_board = Board(game_size)
        self._ship_set = []
        for ship_size in SHIPS_DISTR[game_size]:  # Набор кораблей для этого размера поля забираем из константы в файле ShipsDistribution
            new_ship = Ship(ship_size)  # Создаем объекты класса Корабль разного размера
            self._ship_set.append(new_ship)  # Добавляем в список кораблей игрока

    def random_placement(self, game_size):  # Метод для рандомной расстановки кораблей
        while True:  # Иногда возникают такие ситуации, когда не выходит расставить все корабли по правилам, тк не хватает места.
            for ship in self._ship_set[
                        ::-1]:  # Поэтому я сделал так, чтобы если после 100 попыток не получается расставить корабли, обнуляем доску и начинаем сначала
                ok = False
                iter = 0
                while not ok:
                    iter += 1
                    if iter == 100:
                        break
                    ship.set_position(r.randint(1, game_size),
                                      r.randint(1, game_size))  # Ставим корабль в рандомное место
                    ship.set_orientation(bool(r.getrandbits(1)))
                    try:
                        self.check_on_board(ship, self._my_board)  # Проверяем, можно ли его туда поставить
                    except Exception:
                        pass  # Если ловится выброшенная нами ошибка, то повторяем для следующего рандомного места
                    else:
                        ok = True
                        self.put_the_ship_on_the_board(
                            ship)  # Если получилось поставить, то наносим его на доску и переходим к следующему кораблю
            if ok:
                return True
            self._my_board.reset(game_size)

    def print_all_ships(self):
        print("Список всех кораблей, расставленных на карте:")
        for ship in self._ship_set:
            print("".join(ship.get_body))

    @staticmethod
    def check_on_board(ship, board):  # Статический метод проверки на возможность поставить корабль с такими координатами
        ok = False
        x = ship.get_x_position
        y = ship.get_y_position

        if ship.is_horizontal:
            for i in range(ship.get_size):
                if board.status()[x + i][y] == "◼":
                    raise ValueError("Can't put the tile here")
                MiscFunctions.check_the_board_around_tile(x + i - 1, y - 1, board)
                MiscFunctions.check_the_board_around_tile(x + i - 1, y, board)
                MiscFunctions.check_the_board_around_tile(x + i - 1, y + 1, board)
                MiscFunctions.check_the_board_around_tile(x + i, y - 1, board)
                MiscFunctions.check_the_board_around_tile(x + i, y + 1, board)
                MiscFunctions.check_the_board_around_tile(x + i + 1, y, board)
                MiscFunctions.check_the_board_around_tile(x + i + 1, y - 1, board)
                MiscFunctions.check_the_board_around_tile(x + i + 1, y + 1, board)
        else:
            for i in range(ship.get_size):
                if board.status()[x][y + i] == "◼":
                    raise ValueError("Can't put the tile here")

                MiscFunctions.check_the_board_around_tile(x - 1, y + i - 1, board)
                MiscFunctions.check_the_board_around_tile(x - 1, y + i, board)
                MiscFunctions.check_the_board_around_tile(x - 1, y + i + 1, board)
                MiscFunctions.check_the_board_around_tile(x, y + i - 1, board)
                MiscFunctions.check_the_board_around_tile(x, y + i + 1, board)
                MiscFunctions.check_the_board_around_tile(x + 1, y + i, board)
                MiscFunctions.check_the_board_around_tile(x + 1, y + i - 1, board)
                MiscFunctions.check_the_board_around_tile(x + 1, y + i + 1, board)

    def put_the_ship_on_the_board(self, ship):
        x = ship.get_x_position
        y = ship.get_y_position
        if ship.is_horizontal:
            for i in range(ship.get_size):
                self._my_board.set_tile(x + i, y, "◼")
        else:
            for i in range(ship.get_size):
                self._my_board.set_tile(x, y + i, "◼")

    def set_boards(self, my_board, vs_board):
        self._my_board = my_board
        self._vs_board = vs_board

    @property
    def my_board(self):
        return self._my_board

    @property
    def vs_board(self):
        return self._vs_board

    @property
    def ship_set(self):
        return self._ship_set

    @ship_set.setter
    def ship_set(self, ships):
        self._ship_set = ships

    def ship_is_hit(self, x, y):
        for ship in self._ship_set:
            if ship.is_horizontal:
                if ship.get_y_position == y and (ship.get_x_position <= x <= ship.get_x_position + ship.get_size):
                    ship.set_tile(x - ship.get_x_position, "☒")
                pass
            else:
                if ship.get_x_position == x and (ship.get_y_position <= y <= ship.get_y_position + ship.get_size):
                    ship.set_tile(y - ship.get_y_position, "☒")
                pass

    def is_defeated(self):
        defeat = True
        for ship in self._ship_set:
            for tile in ship.get_body:
                if tile == "◼":  # Пока есть хотя бы одна непораженная ячейка, игрок не проиграл
                    defeat = False

        return defeat

    def ask(self):
        pass

    def move(self):
        pass


class CPU(Player):

    def ask(self):
        return r.randint(1, len(self.vs_board.status()[0])), \
            r.randint(1, len(self.vs_board.status()[0])),

    def move(self, opponent_board):
        cols = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        rows = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                '20',
                '21', '22', '23', '24', '25', '26']
        while True:
            try:
                x, y = self.ask()
                shot_result = opponent_board.shot(x, y)
                self._vs_board.set_tile(x, y, shot_result)
            except WrongShot as e:
                pass
            else:
                if shot_result == "◈":

                    return 1, x, y
                elif shot_result == "☒":
                    return 2, x, y


class User(Player):

    def ask(self):
        cols = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        rows = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                '20',
                '21', '22', '23', '24', '25', '26']

        move = input("Введи координаты точки для выстрела в формате A1: ")

        if move[0].upper() in cols:
            y = cols.index(move[0].upper())
            if move[1:] in rows:
                x = int(move[1:])
                return x, y
            else:
                raise OutOfBounds
        else:
            raise OutOfBounds

    def move(self, opponent_board):
        while True:
            try:
                x, y = self.ask()
                shot_result = opponent_board.shot(x, y)
                self.vs_board.set_tile(x, y, shot_result)
            except Exception as e:
                print(e, "Выберите другую точку!")
            else:
                if shot_result == "◈":

                    return 1, x, y
                elif shot_result == "☒":

                    return 2, x, y


class Ship:  # Класс корабля
    x, y = None, None  # Координаты на доске
    _horizontal = None  # Ориентация (вертикально/горизонтально)
    _size = None  # Размер корабля
    _body = None  # Корпус корабля - список клеток. при пробитии одной из клеток соответствующий символ корпуса будет изменяться

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
    def is_horizontal(self):
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

    def set_tile(self, tile, sign):
        self._body[tile] = sign


class Game:  # Класс игры

    _winner = None  # Победитель, при проверке на победителя будет присваиваться значение 1, если победил игрок, и 2, если победил компьютер
    _user_turn = None  # Очередность хода
    _game_size = None  # Размер поля

    _user = None
    _cpu = None

    def __init__(self):
        self.welcome_text()
        self._game_size = self.set_level()

        self._user = User(False, self._game_size)
        self._cpu = CPU(True, self._game_size)
        self._user_turn = bool(r.getrandbits(1))  # Пока первый ход определяется рандомно


    def welcome_text(self):
        print("\n\n\n\n--- ДОБРО ПОЖАЛОВАТЬ В ИГРУ BATTLE SHIPS CONSOLE ---")
        print("-------------------- Версия 1.2 --------------------")
        print("\n\n                         __/___")
        print("                   _____/______|")
        print("           _______/_____\_______\_____")
        print("           \              < < <       |")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    def set_level(self):
        print("\n\nВведите размер поля (от 2, что соответствует размеру 2х2, до 26, что соответствует размеру 26х26).")
        print("Количество кораблей в игре будет зависеть от размера поля.")
        print("Чем больше поле, тем сложнее и дольше игра.")
        while True:
            try:
                result = int(input ("Введите желаемый размер поля:"))
                if 2 <= result <= 26:
                    return result
                else:
                    print("Неверный ввод, проверьте, что вводите целое число от от 2 до 26")
            except Exception:
                print("Неверный ввод, проверьте, что вводите целое число от от 2 до 26")




    def start(self):
        self.game_play()

    def print_boards(self):  # Метод вывода на экран сразу двух полей

        print("\n",
              " " * int(self._game_size * 1.5), "ТВОЕ ПОЛЕ",
              " " * int(self._game_size * 1.5), "\t\t" * (self._game_size // 3), "ПОЛЕ ПРОТИВНИКА",
              " " * int(self._game_size * 1.5), "\n")
        tmp_board = [[]]
        for i in range(self._game_size + 1):
            tmp_board[i] = self._user.my_board.status()[i].copy()
            for j in range(self._game_size + 1):
                if j == 0:
                    tmp_board[i].append("\t\t\t" + str(self._user.vs_board._board[i][j]))
                else:
                    tmp_board[i].append(str(self._user.vs_board._board[i][j]))
            tmp_board.append([])
        tmp_board.pop()
        print(' |\n'.join(' | '.join(map(str, row)) for row in tmp_board), "|")
        tmp_board.clear()

    def ceremony(self):
        print('\n')
        if self._winner == 1:
            print("Поздравляем, Вы победили!")
        elif self._winner == 2:
            print("Сожалеем, Вы проиграли!")
        else:
            print("Что-то странное случилось, не знаю, кто победил")

    def game_play(self):
        self._user.random_placement(self._game_size)
        self._cpu.random_placement(self._game_size)
        self.print_boards()

        while not self._winner:

            if self._user_turn:
                print("\nТвой ход...\n")
                time.sleep(1)
                move, x, y = self._user.move(self._cpu.my_board)

                if move == 1:
                    print("\n\n-------------МИМО!-------------\n\n")
                    time.sleep(2)
                    self.print_boards()
                    self._cpu.print_all_ships()
                    self._user_turn = not self._user_turn
                elif move == 2:
                    print("\n\n==============ПОПАДАНИЕ!================\n\n")
                    time.sleep(2)
                    self.print_boards()
                    self._cpu.ship_is_hit(x, y)

                    if self._cpu.is_defeated():
                        self._winner = 1

                    self._cpu.print_all_ships()

            else:
                print("\nХод противника...\n")
                time.sleep(3)
                move, x, y = self._cpu.move(self._user.my_board)

                if move == 1:
                    print(f"\n\n-------------{MiscFunctions.xy_to_coord(x, y)}-------------")
                    time.sleep(2)
                    print("\n\n-------------МИМО!-------------\n\n")
                    time.sleep(2)
                    self.print_boards()
                    self._user.print_all_ships()
                    self._user_turn = not self._user_turn
                elif move == 2:
                    print(f"\n\n-------------{MiscFunctions.xy_to_coord(x, y)}-------------")
                    time.sleep(2)
                    print("\n\n==============ПОПАДАНИЕ!================\n\n")
                    time.sleep(2)
                    self._user.ship_is_hit(x, y)
                    self.print_boards()
                    if self._user.is_defeated():
                        self._winner = 2
                    self._user.print_all_ships()


class MiscFunctions:  # Вспомогательный класс, содержащий статические методы
    @staticmethod
    def check_the_board_around_tile(x, y, board):
        try:
            if board.status()[x][y] == "◼":
                raise ValueError("Can't put the tile here")
        except IndexError:
            pass
    @staticmethod
    def xy_to_coord(x, y):
        cols = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        rows = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
            '20', '21', '22', '23', '24', '25', '26']
        return "".join([cols[y], rows[x - 1]])

class Board:
    _board = None

    def __init__(self, size=10):

        chars = " 🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩"
        if size > len(chars) - 1:
            size = len(chars) - 1
        elif size < 2:
            size = 2
        self._board = [["☐" for j in range(size + 1)] for i in range(size + 1)]  # ◈
        for i in range(size + 1):
            self._board[i][0] = " " + str(i) if len(str(i)) < 2 else str(i)
            self._board[0][i] = chars[i] if i > 0 else "  "

    def reset(self, size):
        for i in range(1, size + 1):
            for j in range(1, size + 1):
                self._board[i][j] = "☐"

    def shot(self, x, y):
        try:
            if x == 0 or y == 0:
                raise OutOfBounds
            elif self._board[x][y] == "◈" or self._board[x][y] == "☒":
                raise MultipleShot
            else:
                if self._board[x][y] == "☐":
                    self._board[x][y] = "◈"
                    return "◈"
                elif self._board[x][y] == "◼":
                    self._board[x][y] = "☒"
                    return "☒"
        except IndexError:
            raise OutOfBounds

    def print_board(self):
        print(' |\n'.join(' | '.join(map(str, row)) for row in self._board), "|")

    def status(self):
        return self._board

    def set_tile(self, x, y, value):
        self._board[x][y] = value


class WrongShot(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]

        else:
            self.message = None

    def __str__(self):
        print("Неверный ввод!")
        if self.message:
            return 'MultipleShot, {0} '.format(self.message)
        else:
            return 'WrongShot has been raised'

class OutOfBounds(WrongShot):
    def __str__(self):
        print("Точка за границами поля")
        if self.message:
            return 'OutOfBounds, {0} '.format(self.message)
        else:
            return 'OutOfBounds has been raised'

class MultipleShot(WrongShot):
    def __str__(self):
        print("Это поле уже использовано")
        if self.message:
            return 'MultipleShot, {0} '.format(self.message)
        else:
            return 'MultipleShot has been raised'
