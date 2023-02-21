

def init_field(n=3):   #Инициализируем чистое игровое поле
    field = [["-" for j in range(n+1)] for i in range(n+1)]
    for i in range (n+1):
        field[0][i], field[i][0] = i, i
    field[0][0] = " "
    return field

def print_field(field): #Распечатываем игровое поле
    print('\n'.join('\t'.join(map(str, row)) for row in field))  # Вывести матрицу красиво

def gameplay():






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    game_field = init_field()
    print_field(game_field)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
