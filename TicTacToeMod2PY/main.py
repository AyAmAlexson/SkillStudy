import time


def init_field(n=3):  # Инициализируем чистое игровое поле
    ch = ["0", "A", "B", "C"]
    field = [["-" for j in range(n + 1)] for i in range(n + 1)]
    for i in range(n + 1):
        field[0][i], field[i][0] = ch[i], i
    field[0][0] = " "
    return field


def print_field(field):  # Распечатываем игровое поле
    print('\n'.join('\t'.join(map(str, row)) for row in field))  # Вывести матрицу красиво


def make_move_player(field, char):     #функция запуска хода игрока
    cols = ["a", "b", "c"]
    rows = ["1", "2", "3"]
    while True:
        move = input("Введите поле для вашего хода в формате A1: ")
        if move[0].lower() in cols and move[1] in rows:
            if field[int(move[1])][cols.index(move[0].lower()) + 1] == "-":
                field[int(move[1])][cols.index(move[0].lower()) + 1] = char
                print_field(field)
                return field
            else:
                print("Это поле занято, повторите ввод")

        else:
            print("Неверный ввод поля, повторите ввод")


def make_move_cpu(field, char):
    for i in range(1, 4):
        for j in range(1, 4):
            if field[i][j] == "-":
                field[i][j] = char
                print_field(field)
                return field

    return field


def check_win(field):
    for i in range(1, 4):
        if ((field[i][1] == field[i][2] == field[i][3]) and field[i][1] != "-") or \
                (field[1][i] == field[2][i] == field[3][i] and field[1][i] != "-"):
            return True
        if ((field[1][1] == field[2][2] == field[3][3]) or (field[3][1] == field[2][2] == field[1][3])) and \
                field[2][2] != "-":
            return True
    return False


def check_full(field):
    for i in range(1, 4):
        for j in range(1, 4):
            if field[i][j] == "-":
                return False
    return True


def gameplay(field, player_turn):
    if player_turn:
        player_char, cpu_char = "X", "O"
    else:
        cpu_char, player_char = "X", "O"

    while True:
        if player_turn:
            field = make_move_player(field, player_char)
            if check_win(field):
                return 1
            elif check_full(field):
                return 0
            else:
                player_turn = not player_turn
        else:
            print("Думаю...")
            time.sleep(2)
            field = make_move_cpu(field, cpu_char)

            if check_win(field):
                return 2
            elif check_full(field):
                return 0
            else:
                player_turn = not player_turn


if __name__ == '__main__':
    print('PyCharm')

    game_field = init_field()
    print_field(game_field)
    pl_turn = None
    correct_input = False

    while not correct_input:

        start_choice = input("Желаете начать первым? 1: Да; 2: Нет  ")

        if start_choice == "1":
            pl_turn = True
            correct_input = True
        elif start_choice == "2":
            pl_turn = False
            correct_input = True
        if not correct_input:
            print("Неверный ввод, повторите попытку")

    winner = gameplay(game_field, pl_turn)
    if winner == 1:
        print("Победа!")
    elif winner == 2:
        print("Поражение!")
    else:
        print("Ничья!")
