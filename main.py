import json
import random
import sys
import time
from pydoc import describe

from colorama import init, Fore, Back, Style
with open('data.json', 'r', encoding='utf8') as file:
    data = json.load(file)


words_dict = {}
words_coords = []

def create_grid(size):
    return [['.' for _ in range(size)] for _ in range(size)]


def can_place_word(grid, word, row, col, is_horizontal):
    if row == 0 or col == 0 or row == len(grid) - 1 or col == len(grid[0]) - 1:
        return False
    if len(word) + col >= len(grid[0]) and is_horizontal:
        return False
    if len(word) + row >= len(grid) and not is_horizontal:
        return False

    cross = False
    if grid[row - 1][col] != '.' or grid[row + 1][col] != '.' or grid[row][col + 1] != '.' or grid[row][col - 1] != '.':
        return False
    for i in range(len(word)):
        if row == 0 or col == 0 or col + 1 >= len(grid) or row + 1 >= len(grid):
            return False
        if is_horizontal:
            if col + i == len(grid):
                return False
            if col + i + 1 < len(grid) and i + 1 < len(word):
                if grid[row][col + i] == word[i] and grid[row][col + i + 1] == word[i + 1]:
                    return False
                elif grid[row][col + i] == word[i] and grid[row][col + i + 1] == '.':
                    cross = True
                elif grid[row + 1][col + i] != '.' or grid[row - 1][col + i] != '.':
                    return False

        else:
            if row + i == len(grid):
                return False
            if row + i + 1 < len(grid) and i + 1 < len(word):
                if grid[row + i][col] == word[i] and grid[row + i + 1][col] == word[i + 1]:
                    return False
                elif grid[row + i][col] == word[i] and grid[row + i + 1][col] == '.':
                    cross = True
                elif grid[row + i][col + 1] != '.' or grid[row + i][col - 1] != '.':
                    return False
    if cross is True:
        return True
    else:
        return False


def place_word(grid, word, row, col, is_horizontal):
    words_dict[word] = {'position': is_horizontal,
                        'coords': []}
    for i in range(len(word)):
        if is_horizontal:
            grid[row][col + i] = word[i]
            words_dict[word]['coords'].append((row, col + i))
            words_coords.append((row, col + i))
        else:
            grid[row + i][col] = word[i]
            words_dict[word]['coords'].append((row + i, col))
            words_coords.append((row + i, col))


def generate_crossword(words, size=20):
    grid = create_grid(size)
    while True:
        first_word = random.choice(words)
        if len(first_word) >= 12:
            break
    place_word(grid, first_word, size // 2, (size - len(first_word)) // 2, True)
    del words[words.index(first_word)]
    sc = 0
    while sc != 6:
        word = random.choice(words)
        placed = False
        for i in range(400):
            row = random.randint(0, size - 1)
            col = random.randint(0, size - 1)
            orientation = random.choice([True, False])
            if can_place_word(grid, word, row, col, orientation):
                place_word(grid, word, row, col, orientation)
                placed = True
                sc += 1
                del words[words.index(word)]
                break
    return grid


def print_crossword(grid):
    for index, row in enumerate(grid):
        if index < 10:
            print(Fore.LIGHTWHITE_EX + f"{index}  {'  '.join(row)}")
        else:
            print(Fore.LIGHTWHITE_EX + f"{index} {'  '.join(row)}")
        time.sleep(0.05)
    print(Fore.LIGHTWHITE_EX + '   0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19')



def mask_grid(grid, size=20):
    masked_grid = [[Fore.LIGHTWHITE_EX + '.' for _ in range(20)] for _ in range(20)]
    for i in range(20):
        for j in range(20):
            if grid[i][j] != '.':
                masked_grid[i][j] = Fore.RED + '⊞'
    return masked_grid

# def unmask_grid(grid, size=20):
#     for i in range(20):
#         for j in range(20):
#             if grid[i][j] == '⊞':


words = list(filter(lambda x: len(x.split()) == 1, list(data.keys())))
# print(words)
grid = generate_crossword(words)
# print(words_dict)
# print(words_coords)
masked_grid = mask_grid(grid)
print_crossword(masked_grid)
print_crossword(grid)




def get_word(row, col):
    if row > 19 or row < 0 or col > 19 or col < 0:
        print(Fore.RED + 'Такой координаты не существует')
        main_menu()
    let = grid[row][col]
    targets = {}
    if let != '.':
        for i in words_dict:
            if (row, col) in words_dict[i]['coords']:
                targets[words_dict[i]['position']] = i
        if len(targets) == 2:
            print(Fore.LIGHTWHITE_EX + 'Здесь 2 слова, хотите выбрать по горизонтали или вертикали? ("г" - по-горизонтали | "в" - по-вертикали)')
            orientation = input(Fore.LIGHTWHITE_EX)
            if orientation.lower() == 'г':
                return data[targets[True]], True, targets[True]
            elif orientation.lower() == 'в':
                return data[targets[False]], True, targets[False]
        else:
            return data[list(targets.values())[0]], True, list(targets.values())[0]
    else:
        return ('Слова на такой координате нету', False)


def open_word(word):
    for i in words_dict[word]['coords']:
        masked_grid[i[0]][i[1]] = Fore.GREEN + word[words_dict[word]['coords'].index(i)]
    del words_dict[word]
    print_crossword(masked_grid)
    print(Fore.LIGHTWHITE_EX + '---------------------------------------------------')
    time.sleep(1)
    main_menu()

def guess_word(correct_word):
    print(Fore.LIGHTWHITE_EX + 'Итак, введите слово:')
    print(correct_word)
    word = input(Fore.WHITE)
    if word.lower() == correct_word.lower():
        print(Fore.GREEN + 'Ого! Вы отгадали данное слово')
        open_word(correct_word)
    else:
        print(Fore.LIGHTWHITE_EX + 'К сожалению, это не то слово....')
        print(Fore.LIGHTWHITE_EX + '---------------------------------------------------')
        time.sleep(1)
        incorrect_guess(correct_word)

def incorrect_guess(correct_word):
    print(Fore.LIGHTWHITE_EX + '("д" - продолжить отгадывать слово | "н" - выйти в главное меню)')
    cmd = input(Fore.LIGHTWHITE_EX)
    if cmd == 'д':
        guess_word(correct_word)
    elif cmd == 'н':
        main_menu()
    else:
        print(Fore.LIGHTWHITE_EX + 'такой команды не существует')
        print(Fore.LIGHTWHITE_EX + '---------------------------------------------------')
        time.sleep(1)
        incorrect_guess(correct_word)

def try_guess(word):
    print(Fore.LIGHTWHITE_EX + 'Хотите отгадать слово? ("д" - да, "н" - нет)')
    a = input()
    if a == 'д':
        guess_word(word)
    elif a == 'н':
        main_menu()
    else:
        print(Fore.RED + 'такой команды не существует')
        print(Fore.LIGHTWHITE_EX + '---------------------------------------------------')
        time.sleep(1)
        try_guess(word)


def main_menu():
    print(words_dict)
    if words_dict == {}:
        print(Fore.GREEN + 'Поздравляем, вы выиграли!!!')
        return
    print(Fore.LIGHTWHITE_EX + 'Введите одну координату слова')
    i = input(Fore.LIGHTWHITE_EX)
    coords = i.split()
    try:
        result = get_word(int(coords[0]), int(coords[1]))
    except Exception:
        print(Fore.RED + 'Неверный формат ввода')
        main_menu()
    describtion = result[0].replace('. ', '\n')
    print(describtion)
    if result[1] == True:
        try_guess(result[2])
    else:
        print(Fore.LIGHTWHITE_EX + '---------------------------------------------------')
        time.sleep(1)
        main_menu()

main_menu()
# print('\n'.join([data[i] for i in words_coords.keys()]))

