import pygame, sys
from pygame.locals import *
import random
import PIL
from PIL import Image
import itertools
import time


### FIX THE RATIOS FOR THE ICONS AT THE TOP


pygame.init()

def home_page():
    display_surface = pygame.display.set_mode((500, 500))
    display_surface.fill((0, 0, 0))
    pygame.display.set_caption('Minesweeper!')
    white = (255, 255, 255)
    text = ('Challenge Awaits!', 'Easy', 'Medium', 'Hard')
    for i in range(4):
        text_font = pygame.font.Font('freesansbold.ttf', 30)
        textSurface = text_font.render(text[i], True, white)
        TextSurf, TextRect = textSurface, textSurface.get_rect()
        TextRect.center = (250, 100 + 100*i)
        display_surface.blit(TextSurf, TextRect)
    while True:
        for event in pygame.event.get():
            pygame.display.update()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                if 150 < mousex < 300 and 150 < mousey < 250:
                    print('yay!')
                    difficulty = 'Easy'
                    main(difficulty)
                if 120 < mousex < 330 and 250 < mousey < 350:
                    difficulty = 'Medium'
                    main(difficulty)
                if 150 < mousex < 300 and 350 < mousey < 450:
                    difficulty = 'Hard'
                    main(difficulty)

def new_game(board):
    board.set_board()
    bomb_count = board.mines
    game_clock = 0
    tile_list, score_list = pygame.sprite.Group(), pygame.sprite.Group()
    score_dude = Score_Person(board.width)
    bomb_tens_digit = Bomb_Number(str(bomb_count)[0], board.width * 4)
    bomb_ones_digit = Bomb_Number(str(bomb_count)[1], board.width * 4 + 13)
    time_hundreds_digit  = Time_Number(game_clock, board.width * 12 + 18)
    time_tens_digit = Time_Number(game_clock, board.width * 12 + 31)
    time_ones_digit = Time_Number(game_clock, board.width * 12 + 44)

    # list of all numbers, smiley faces
    score_sprites = (score_dude, bomb_tens_digit, bomb_ones_digit,
                     time_ones_digit, time_tens_digit, time_hundreds_digit)

    # put them all in one list
    for sprite in score_sprites:
        score_list.add(sprite)

    # tile sprites for board
    for row in range(board.height):
        for col in range(board.width):
            block = Bomb_Tile('box_signs0', row, col, board.board_matrix[row][col])
            tile_list.add(block)

    #game clock defaults, game state
    start = time.perf_counter()
    end_game = False
    first_move = True

    return board, tile_list, score_list, start, end_game, first_move, bomb_count

def main(difficulty):
    # setting the difficulty of the board (changes the # of mines, the size of the board)
    board = Board(difficulty)
    display_surface = pygame.display.set_mode((board.width * 16 + 50, board.height * 16 + 75))
    display_surface.fill((0, 0, 0))
    pygame.display.set_caption('Minesweeper!')

    board, tile_list, score_list, start, end_game, first_move, bomb_count = new_game(board)

    # some other constants to avoid undefined variables
    initial_time = 0
    mousex, mousey =  250, 250
    row, col = -1, -1

    #location of smiley face
    smiley_left = board.width * 8 + 13
    smiley_right = board.width * 8 + 39
    smiley_top = 12
    smiley_bottom = 40

    while True:
        if end_game is False:
            game_clock = int(time.perf_counter() - start)
            if 0 < game_clock < 999:
                if game_clock < 10:
                    game_clock = '00' + str(game_clock)
                elif game_clock < 100:
                    game_clock = '0' + str(game_clock)
                update_score(score_list, [sprite for sprite in score_list][3:],
                            game_clock, board.width * 12 + 18, 'time')
            score_list.draw(display_surface)
            pygame.display.update()
        for event in pygame.event.get():
            count = 0
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                initial_time = time.perf_counter()
                mousex, mousey = event.pos
                if smiley_left < mousex < smiley_right and smiley_top < mousey < smiley_bottom:
                    [sprite for sprite in score_list][0].clicked()
                    end_game = True
                elif end_game is False:
                    row, col = int((mousey - 50)/16), int((mousex - 25) /16)
                    for tile in tile_list:
                        if tile.name ==  'block' + str(row) + ',' + str(col):
                            tile.dampen()
                            selected_tile = tile

            elif event.type == MOUSEBUTTONUP:
                if 0 <= row < board.height and 0 <= col < board.width and end_game is False:
                    final_time = time.perf_counter()
                    if final_time - initial_time < .15 and selected_tile.flagged is False:
                        if selected_tile.mine is True:
                            if first_move is False:
                                selected_tile.explode()
                                end_game = True
                                [sprite for sprite in score_list][0].loss()
                                for tile in tile_list:
                                    if tile != selected_tile:
                                        if tile.mine is True:
                                            tile.bomb_reveal()
                                        elif tile.flagged is True:
                                            tile.false_flag_reveal()
                            else:
                                first_move = False
                                board.fix_first_move(row, col)
                                tile_list = pygame.sprite.Group()
                                sprite_board(board, tile_list)
                                check_move(board, row, col, tile_list)

                        else:
                            if first_move == True:
                                first_move = False
                            check_move(board, row, col, tile_list)

                    else:
                        if initial_time > 0:
                            if selected_tile.flagged is False:
                                selected_tile.flag()
                                bomb_count -= 1
                                if bomb_count < 10:
                                    bomb_count = '0' + str(bomb_count)
                                else:
                                    bomb_count = str(bomb_count)
                                update_score(score_list, [sprite for sprite in score_list][1:3],
                                             bomb_count, board.width * 4, 'bomb')
                                bomb_count = int(bomb_count)
                            else:
                                selected_tile.unflag()
                                bomb_count += 1
                                if bomb_count < 10:
                                    bomb_count = '0' + str(bomb_count)
                                update_score(score_list, [sprite for sprite in score_list][1:3],
                                             bomb_count, board.width * 4, 'bomb')
                                bomb_count = int(bomb_count)

                for tile in tile_list:
                    if tile.mine == True:
                        if tile.flagged == True:
                            count += 1
                    else:
                        if tile.reveal == True:
                            count += 1

                if count == len(board.board_matrix)*len(board.board_matrix[0]):
                    end_game = True
                    [sprite for sprite in score_list][0].win()

                if end_game is True and board.width * 8 + 13 < mousex < board.width * 8 + 39 and 12 < mousey < 40:
                    board.reset(difficulty)
                    board, tile_list, score_list, start, end_game, first_move, bomb_count = new_game(board)

            tile_list.draw(display_surface)
            score_list.draw(display_surface)
            pygame.display.update()


class Board(pygame.sprite.Sprite):
    def __init__(self, difficulty):
        pygame.sprite.Sprite.__init__(self)
        if difficulty == 'Easy':
            self.width, self.height, self.mines = 9, 9, 10
        elif difficulty == 'Medium':
            self.width, self.height, self.mines = 16, 16, 40
        elif difficulty == 'Hard':
            self.width, self.height, self.mines = 30, 16, 99
        self.board_matrix = [[0 for column in range(self.width)] for row in range(self.height)]

    def reset(self, difficulty):
        if difficulty == 'Easy':
            self.width, self.height, self.mines = 9, 9, 10
        elif difficulty == 'Medium':
            self.width, self.height, self.mines = 16, 16, 40
        elif difficulty == 'Hard':
            self.width, self.height, self.mines = 30, 16, 99
        self.board_matrix = [[0 for column in range(self.width)] for row in range(self.height)]

    def set_board(self):
        mine_placed = 0
        while mine_placed < self.mines:
            mine_row = random.randint(0, self.height - 1)
            mine_column = random.randint(0, self.width - 1)
            if self.board_matrix[mine_row][mine_column] == 0:
                self.board_matrix[mine_row][mine_column] = 'Mine'
                mine_placed += 1
        for row in range(self.height):
            for col in range(self.width):
                if self.board_matrix[row][col] != 'Mine':
                    self.board_matrix[row][col] = self.count_mines(row, col)

    def count_mines(self, row, col):
        count = 0
        permutation_list = [-1, 0, 1]
        row_list, col_list, att_list = [], [], []
        for test_number in permutation_list:
            if 0 <= row + test_number < len(self.board_matrix):
                row_list.append(test_number)
            if 0 <= col + test_number < len(self.board_matrix[0]):
                col_list.append(test_number)
        for add_subtract in itertools.permutations((-1, -1, 0, 1, 1), 2):
            if add_subtract[0] in row_list and add_subtract[1] in col_list and add_subtract not in att_list:
                if self.board_matrix[row + add_subtract[0]][col + add_subtract[1]] == 'Mine':
                    count += 1
                att_list.append(add_subtract)
        return count

    def check_blocks(self, initial, direction = 0, step = 0, empty_list = [],
                   reveal_list = [], directions = {0: (0, 1), 1: (1, 1), 2:(1,0), 3:(1, -1),
                      4:(0, -1), 5:(-1, -1), 6:(-1, 0), 7:(-1, 1)}, key = {0: 'right', 1: 'bot_right',
                    2: 'bottom', 3:'bot_left', 4:'left', 5:'up_left', 6:'up', 7:'up_right'}):
        if 7 < step:
            return empty_list, reveal_list
        if 7 < direction:
            direction = 0
        row = initial[0] + directions[direction][0]
        col = initial[1] + directions[direction][1]
        if 0 <= row < len(self.board_matrix) and 0 <= col < len(self.board_matrix[0]):
            if (row, col) not in empty_list:
                print(initial, key[direction], (row, col), self.board_matrix[row][col])
                if self.board_matrix[row][col] == 0:
                    return self.check_blocks((row, col), direction, 0, empty_list + [initial],
                             reveal_list)
                if initial not in empty_list:
                    return self.check_blocks(initial, direction + 1, step + 1,
                                             empty_list + [initial], reveal_list + [(row, col)])
                if (row, col) not in reveal_list:
                    return self.check_blocks(initial, direction + 1, step + 1,
                         empty_list, reveal_list + [(row, col)])
            if initial not in empty_list:
                return self.check_blocks(initial, direction + 1, step + 1,
                                         empty_list + [initial], reveal_list)
        return self.check_blocks(initial, direction + 1, step + 1,
                         empty_list, reveal_list)

    def check_all(self, initial):
        empty_list, reveal_list = self.check_blocks(initial)
        to_check_list = list(tuple(empty_list))
        while to_check_list != []:
            delete_length = len(to_check_list)
            for entry in range(delete_length):
                new_empty, new_reveal = self.check_blocks(to_check_list[entry], direction = 0, step = 0,
                                                          empty_list = empty_list, reveal_list = reveal_list)
                for entry in new_empty:
                    if entry not in empty_list:
                        empty_list = empty_list + [entry]
                        to_check_list = to_check_list + [entry]
                for entry in new_reveal:
                    if entry not in reveal_list:
                        reveal_list = reveal_list + [entry]
            to_check_list = to_check_list[delete_length:]
        return empty_list, reveal_list

    def fix_first_move(self, row, col):
        self.board_matrix[row][col] = 0
        while True:
            replace_row, replace_col = random.randint(0, self.height - 1), \
                                       random.randint(0, self.width - 1)
            if (replace_row, replace_col) != (row, col) and \
                    self.board_matrix[replace_row][replace_col] != 'Mine':
                self.board_matrix[replace_row][replace_col] = 'Mine'
                break
        for row in range(self.height):
            for col in range(self.width):
                if self.board_matrix[row][col] != 'Mine':
                    self.board_matrix[row][col] = self.count_mines(row, col)


def check_move(board, row, col, tile_list):
    if board.board_matrix[row][col] == 0:
        empty_list, reveal_list = board.check_all((row, col))
        check_list = empty_list + reveal_list
        for entry in check_list:
            for tile in tile_list:
                if tile.name == 'block' + str(entry[0]) + ',' + str(entry[1]):
                    if tile.flagged is False:
                        tile.reveal_number()
    else:
        for tile in tile_list:
            if tile.name == 'block' + str(row) + ',' + str(col):
                tile.reveal_number()


def sprite_board(board, tile_list):
    for iter_row in range(board.height):
        for iter_col in range(board.width):
            block = Bomb_Tile('box_signs0', iter_row, iter_col,
                              board.board_matrix[iter_row][iter_col])
            tile_list.add(block)


class Bomb_Tile(pygame.sprite.Sprite):
    def __init__(self, name, row, col, number):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'block' + str(row) + ',' + str(col)
        self.image = pygame.image.load('box_signs0.png')
        self.rect = self.image.get_rect()
        self.rect.x = col * 16 + 25
        self.rect.y = row * 16 + 50
        self.number = number
        self.reveal = False
        self.flagged = False
        self.check = 0
        if number == 'Mine':
            self.mine = True
        else:
            self.mine = False

    def explode(self):
        self.image = pygame.image.load('box_signs2.png')

    def reveal_number(self):
        if self.number != 'Mine' and self.reveal is False:
            self.image = pygame.image.load('box_num' + str(self.number) + '.png')
        self.reveal = True

    def dampen(self):
        if self.reveal is False:
            self.image = pygame.image.load('box_num0.png')

    def flag(self):
        self.flagged = True
        self.image = pygame.image.load('box_signs1.png')

    def unflag(self):
        self.flagged = False
        if self.reveal is False and self.check == 0:
            self.image = pygame.image.load('box_signs0.png')
            self.check += 1
        else:
            self.image = pygame.image.load('box_num' + str(self.number) + '.png')

    def bomb_reveal(self):
        self.image = pygame.image.load('box_signs4.png')

    def false_flag_reveal(self):
        self.image = pygame.image.load('box_signs3.png')



class Score_Person(pygame.sprite.Sprite):
    def __init__(self, board_width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('smiley_faces0.png')
        self.rect = self.image.get_rect()
        self.rect.x = board_width*8 + 13
        self.rect.y = 12

    def excited(self):
        self.image = pygame.image.load('smiley_faces2.png')

    def win(self):
        self.image = pygame.image.load('smiley_faces4.png')

    def loss(self):
        self.image = pygame.image.load('smiley_faces3.png')

    def clicked(self):
        self.image = pygame.image.load('smiley_faces1.png')


class Bomb_Number(pygame.sprite.Sprite):
    def __init__(self, number, x_coordinate):
        pygame.sprite.Sprite.__init__(self)
        self.number = str(number)
        self.image = pygame.image.load('count_num' + str(self.number) + '.png')
        self.rect = self.image.get_rect()
        self.rect.x = x_coordinate
        self.rect.y = 12


class Time_Number(pygame.sprite.Sprite):
    def __init__(self, number, x_coordinate):
        pygame.sprite.Sprite.__init__(self)
        self.number = str(number)
        self.image = pygame.image.load('count_num' + str(self.number) + '.png')
        self.rect = self.image.get_rect()
        self.rect.x = x_coordinate
        self.rect.y = 12


def update_score(score_list, object_list, game_value, x_coordinate, type):
    for i in range(len(object_list)):
        score_list.remove(object_list[i])
        if type == 'Time':
            object = Time_Number(str(game_value)[i], x_coordinate + 13*i)
        else:
            object = Bomb_Number(str(game_value)[i], x_coordinate + 13 * i)
        score_list.add(object)
    return score_list


def crop_images():
    image = Image.open('minesweeper.png')
    for i in range(10):
        croppedIm = image.crop((13*i, 0, 13 + 13*i, 23))
        croppedIm.save('count_num' + str(i) + '.png')
    for i in range(9):
        croppedIm = image.crop((16*i, 23, 16 + 16*i, 39))
        croppedIm.save('box_num' + str(i) + '.png')
    for i in range(7):
        croppedIm = image.crop((16 * i, 39, 16 + 16 * i, 55))
        croppedIm.save('box_signs' + str(i) + '.png')
    for i in range(5):
        croppedIm = image.crop((26*i, 55, 26 + 26*i, 80))
        croppedIm.save('smiley_faces' + str(i) + '.png')
    croppedIm = image.crop((26*1, 55, 27 + 26*1, 81))
    croppedIm.save('smiley_faces' + str(1) + '.png')


home_page()
