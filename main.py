import json
import random
import time
import numpy as np

import pygame
import screeninfo
with open('data.json', 'r', encoding='utf8') as file:
    data = json.load(file)

words_dict = {}
words_coords = []

def create_grid():
    return np.full((20, 20), '.')


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


def generate_crossword(words, n, size=20):
    grid = create_grid()
    while True:
        first_word = random.choice(words)
        if len(first_word) >= 12:
            break
    place_word(grid, first_word, size // 2, (size - len(first_word)) // 2, True)
    del words[words.index(first_word)]
    sc = 0
    while sc != n:
        word = random.choice(words)
        for i in range(400):
            row = random.randint(0, size - 1)
            col = random.randint(0, size - 1)
            orientation = random.choice([True, False])
            if can_place_word(grid, word, row, col, orientation):
                place_word(grid, word, row, col, orientation)
                sc += 1
                del words[words.index(word)]
                break
    return grid


def print_crossword(grid):
    for index, row in enumerate(grid):
        if index < 10:
            print(f"{index}  {'  '.join(row)}")
        else:
            print(f"{index} {'  '.join(row)}")
        time.sleep(0.05)
    print('   0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19')


def mask_grid(grid, size=20):
    masked_grid = [['.' for _ in range(20)] for _ in range(20)]
    for i in range(20):
        for j in range(20):
            if grid[i][j] != '.':
                masked_grid[i][j] = '0'
    return masked_grid



def open_word(word):
    for i in words_dict[word]['coords']:
        masked_grid[i[0]][i[1]] =word[words_dict[word]['coords'].index(i)]
    del words_dict[word]
    # print_crossword(masked_grid)
    print('---------------------------------------------------')
    # main_menu()



words = list(filter(lambda x: len(x.split()) == 1, list(data.keys())))
grid = generate_crossword(words, 5)
alpha = 'йцукенгшщзхъфывапролджэячсмитьбюё'
masked_grid = mask_grid(grid)
# print_crossword(masked_grid)


class Input_box:
    def __init__(self, text, posx, posy):
        self.text = text
        self.text_font = Text(self.text, posx + 10, posy + 17, (width + height) // 42, (255, 255, 255))
        self.input_box = pygame.Rect(posx, posy - 3, width / 13, height / 12)
        self.ishidden = True
        self.active = False


    def render(self):
        self.border_color = 'grey' if self.active is False else 'blue'
        if self.ishidden is False:
            mp = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if self.input_box.collidepoint(mp):
                    self.text_font.text = ''
                    self.active = True
                else:
                    self.active = False
            self.text_font.text = self.text
            width = max(200, self.text_font.rendered_text.get_width() + 10)
            self.input_box.w = width
            pygame.draw.rect(screen, self.border_color, self.input_box, 2)
            self.text_font.render()


class Button(pygame.sprite.Sprite):
    def __init__(self, posx, posy, text, color, text_color):
        super().__init__(buttons)
        self.posx = posx
        self.posy = posy
        self.ishidden = True
        self.color = color
        self.text = Text(text, self.posx + (width / 7.68) // 10, self.posy + (height / 10.8) // 4, (width + height) // 75, text_color)
        self.box = pygame.surface.Surface((width / 7.68, height / 10.8))
        self.buttonRect = pygame.Rect(self.posx, self.posy, width / 7.68, height / 10.8)


    def update(self):
        global word
        if self.ishidden is False:
            self.box.fill(self.color)
            screen.blit(self.box, (self.posx, self.posy))
            self.text.render()
        else:
            self.color = [50, 50, 50]
        mp = pygame.mouse.get_pos()
        if self.buttonRect.collidepoint(mp) and self.ishidden is False:
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.color[-1] = 200
                self.box.fill(self.color)
                if self.text.text == 'Угадать слово':
                    input_box.ishidden = False
                elif self.text.text == 'Выбрать направление':
                    horizontal_button.ishidden = False
                    vertical_button.ishidden = False
                elif self.text.text == 'Горизонтальное':
                    if brd.get_word(word[0] + 1, word[2]) is None:
                        word = brd.get_word(word[0] - 1, word[2])
                    else:
                        word = brd.get_word(word[0] + 1, word[2])
                    title.text = word[0]
                    horizontal_button.ishidden = True
                    vertical_button.ishidden = True
                    choose_orientation_btn.ishidden = True
                elif self.text.text == 'Вертикальное':
                    if brd.get_word(word[0], word[2] + 1) is None:
                        word = brd.get_word(word[0], word[2] - 1)
                    else:
                        word = brd.get_word(word[0], word[2] + 1)
                    title.text = word[0]
                    horizontal_button.ishidden = True
                    vertical_button.ishidden = True
                    choose_orientation_btn.ishidden = True

            else:
                self.color = [50, 50, 50]




class Text:
    def __init__(self, text, posx, posy, size, color, feed=False):
        self.feed = feed
        self.posx = posx
        self.posy = posy
        self.text = text
        self.font = pygame.font.SysFont('Cooper', size)
        self.color = color

        self.rendered_text = self.font.render(self.text, 1, color)


    def render(self):
        if self.text in [i.text.text for i in buttons.sprites()]:
            words = self.text.split()
            for word in range(len(words)):
                self.rendered_text = self.font.render(words[word], 1, self.color)
                screen.blit(self.rendered_text, (self.posx, self.posy + 30 * word))
        elif self.feed is False:
            self.rendered_text = self.font.render(self.text, 1, self.color)
            screen.blit(self.rendered_text, (self.posx, self.posy))
        elif self.feed is True and len(self.text) >= 20:
            width = 0
            top = 0
            words = self.text.split()
            for word in range(len(words)):
                self.rendered_text = self.font.render(words[word], 1, self.color)
                screen.blit(self.rendered_text, (self.posx + width, self.posy + top))
                width += self.font.render(words[word] + '  ', 1, (0, 0, 0)).get_width()
                if word + 1 < len(words):
                    if width + self.font.render(words[word + 1] + '  ', 1, (0, 0, 0)).get_width() >= 800:
                        top += 40
                        width = 0





class Board:
    def __init__(self, left, top, cell_size):
        self.board = masked_grid
        self.left = left
        self.top = top
        self.cell_size = cell_size



    def get_cell(self, mouse_pos):
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                cell_coords = (self.cell_size * x + self.left, self.cell_size * y + self.top)
                if (mouse_pos[0] > cell_coords[0] and mouse_pos[0] < cell_coords[0] + self.cell_size and
                        mouse_pos[1] > cell_coords[1] and mouse_pos[1] < cell_coords[1] + self.cell_size):
                    return x, y


    def render(self):
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                if self.board[x][y] == '0':
                    pygame.draw.rect(screen, 'red', (
                        self.left + x * self.cell_size + 2, self.top + y * self.cell_size + 2, self.cell_size - 2, self.cell_size - 2),
                                     )
                elif self.board[x][y] == '1':
                    pygame.draw.rect(screen, (200, 200, 200), (
                        self.left + x * self.cell_size + 2, self.top + y * self.cell_size + 2, self.cell_size - 2, self.cell_size - 2))
                elif self.board[x][y] != '.':
                    text = Text(self.board[x][y], self.left + x * self.cell_size + self.cell_size // 8, self.top + y * self.cell_size + self.cell_size // 10, self.cell_size + 10, (255, 0, 0))
                    text.render()
                # elif self.board[x][y] == '1':
                #     pygame.draw.rect(screen, 'blue', (
                #         self.left + x * self.cell_size + 2, self.top + y * self.cell_size + 2, self.cell_size - 2, self.cell_size - 2))

                pygame.draw.rect(screen, 'black', (
                self.left + x * self.cell_size, self.top + y * self.cell_size, self.cell_size, self.cell_size), width=3)



    def get_word(self, row, col):
        let = grid[row][col]
        targets = {}
        if let != '.' and masked_grid[row][col] != let:
            for i in words_dict:
                if (row, col) in words_dict[i]['coords']:
                    targets[words_dict[i]['position']] = i
            if len(targets) == 2:
                choose_orientation_btn.ishidden = False
                return row, False, col
            else:
                guess_word_btn.ishidden = False
                self.paint_word(list(targets.values())[0])
                return data[list(targets.values())[0]], True, list(targets.values())[0]
        else:
            return None

    def paint(self, x, y):
        self.board[x][y] = '1'


    def paint_word(self, word):
        for i in words_dict[word]['coords']:
            if self.board[i[0]][i[1]] == '0': self.board[i[0]][i[1]] = '1'
            self.render()




    def clear(self):
        title.text = ''
        status.text = ''
        flag = False
        input_box.active = False
        for i in buttons.sprites():
            i.ishidden = True
        input_box.ishidden = True
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                if self.board[x][y] == '1':
                    self.board[x][y] = '0'


def guess_word(word, correct_word):
    print('Итак, введите слово:')
    if word.lower() == correct_word.lower():
        print(words_dict)
        status.text = 'Ого! Вы отгадали данное слово'
        open_word(correct_word)
        if words_dict == {}:
            status.text = 'Поздравляю, вы победили!'
    else:
        status.text = 'Неправильно'



for i in screeninfo.get_monitors():
    height, width = i.height, i.width
    break

size = width, height = 1920, 1080
brd = Board(10, 50, (width + height) // 60)
pygame.init()

screen = pygame.display.set_mode(size)
space = pygame.image.load('фон космоса.jpg')
space = pygame.transform.scale(space, (width, height))
title = Text('', width // 1.84, height // 54 + 50, (width + height) // 50, (255, 255, 255), True)
running = True
buttons = pygame.sprite.Group()
status = Text('', width // 1.84, height // 54 + 320, (width + height) // 50, (255, 255, 255), False)
guess_word_btn = Button(width // 1.84, height // 54 + 400, 'Угадать слово', [50, 50, 50], (255, 255, 255), )
choose_orientation_btn = Button(width // 1.84, height // 54 + 400, 'Выбрать направление', [50, 50, 50], (255, 255, 255))
horizontal_button = Button(width // 1.84, 300, 'Горизонтальное', [50, 50, 50], (255, 255, 255))
vertical_button = Button(width // 1.84 + 275, 300, 'Вертикальное', [50, 50, 50], (255, 255, 255))
description = Text('Описание: ', width // 1.84, height // 54, (width + height) // 50, (255, 255, 255))
input_box = Input_box('', width // 1.84, height // 54 + 200)
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if input_box.active:
                if key[pygame.K_RETURN]:
                    guess_word(input_box.text, word[-1])
                    input_box.text = ''
                elif key[pygame.K_BACKSPACE]:
                    input_box.text = input_box.text[:-1]
                else:
                    input_box.text += event.unicode
            if key[pygame.K_LSHIFT]:
                brd.board = grid
        elif event.type == pygame.KEYUP:
            brd.board = masked_grid
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = brd.get_cell(event.pos)
                if pos:
                    if brd.get_word(*pos):
                        word = brd.get_word(*pos)
                        if word[1] is True:
                            brd.clear()
                            brd.paint(*pos)
                            title.text = brd.get_word(*pos)[0]
                        elif word[1] is False:
                            brd.clear()
                            brd.paint(*pos)
                            brd.get_word(*pos)


    screen.fill((255,255,255))
    screen.blit(space, (0, 0))
    brd.render()
    title.render()
    buttons.update()
    input_box.render()
    description.render()
    status.render()

    clock.tick(30)
    pygame.display.flip()
pygame.quit()
