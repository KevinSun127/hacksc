import pygame, sys
from pygame.locals import *
import time
import random


def main():
    global directions

    directions = {'right': (25, 0), 'left': (-25, 0), 'down': (0, 25),
                  'up': (0, -25)}

    pygame.init()
    display_surface = pygame.display.set_mode((800, 400))
    display_surface.fill((0, 0, 0))
    pygame.display.set_caption('Snake')

    snake = pygame.sprite.Group()
    apples = pygame.sprite.Group()
    moving_piece = pygame.sprite.Group()
    collide_snake = pygame.sprite.Group()

    snake_piece = Snake_Block((400, 200))
    apple_piece = Apple((200, 100))

    SCORE = 0

    moving_piece.add(snake_piece)
    apples.add(apple_piece)

    direction = directions['left']

    start = time.perf_counter()

    end_game = False

    moving_piece.draw(display_surface)
    apples.draw(display_surface)
    pygame.display.update()




    while True:
        if end_game is False:
            game_clock = time.perf_counter() - start
            if 0.1 <= game_clock:
                # move the snake in a direction
                if len(snake) > 0:
                    i = 0
                    for block in snake:
                        i += 1
                        if i == 1:
                            test_block_2 = block
                    snake.remove(test_block_2)
                    snake.add(snake_piece)

                    moving_piece.remove(snake_piece)
                    if 0 < snake_piece.rect.x + direction[0] < 800 and \
                        0 < snake_piece.rect.y + direction[1] < 400:
                        snake_piece = Snake_Block((snake_piece.rect.x + direction[0],
                                               snake_piece.rect.y + direction[1]))
                    else:
                        if direction == directions['right']:
                            snake_piece = Snake_Block((direction[0], snake_piece.rect.y))
                        elif direction == directions['left']:
                            snake_piece = Snake_Block((800 + direction[0], snake_piece.rect.y))
                        elif direction == directions['up']:
                            snake_piece = Snake_Block((snake_piece.rect.x, 400 + direction[1]))
                        else:
                            snake_piece = Snake_Block((snake_piece.rect.x, direction[1]))
                    moving_piece.add(snake_piece)

                else:
                    X = snake_piece.rect.x
                    Y = snake_piece.rect.y
                    moving_piece.remove(snake_piece)
                    if 0 < X + direction[0] < 800 and \
                        0 < Y + direction[1] < 400:
                        snake_piece = Snake_Block((X + direction[0],
                                                   Y + direction[1]))
                    else:
                        if direction == directions['right']:
                            snake_piece = Snake_Block((direction[0], snake_piece.rect.y))
                        elif direction == directions['left']:
                            snake_piece = Snake_Block((800 + direction[0], snake_piece.rect.y))
                        elif direction == directions['up']:
                            snake_piece = Snake_Block((snake_piece.rect.x, 400 + direction[1]))
                        else:
                            snake_piece = Snake_Block((snake_piece.rect.x, direction[1]))
                    moving_piece.add(snake_piece)
                start = time.perf_counter()
                display_surface.fill((0, 0, 0))
                apples.draw(display_surface)
                snake.draw(display_surface)
                moving_piece.draw(display_surface)
                TextSurf, TextRect = white_score_board(SCORE)
                display_surface.blit(TextSurf, TextRect)
                pygame.display.update()
            for block in collide_snake:
                collide_snake.remove(block)
            i = 0
            for block in snake:
                i += 1
                if i != len(snake):
                    collide_snake.add(block)
            if pygame.sprite.spritecollide(snake_piece, collide_snake, False):
                end_game = True

        else:
            display_surface = pygame.display.set_mode((800, 400))
            display_surface.fill((0, 0, 0))
            snake = pygame.sprite.Group()
            apples = pygame.sprite.Group()
            moving_piece = pygame.sprite.Group()
            collide_snake = pygame.sprite.Group()
            snake_piece = Snake_Block((400, 200))
            apple_piece = Apple((200, 100))
            moving_piece.add(snake_piece)
            apples.add(apple_piece)
            direction = directions['left']
            start = time.perf_counter()
            end_game = False
            SCORE = 0
            moving_piece.draw(display_surface)
            apples.draw(display_surface)
            pygame.display.update()

        if pygame.sprite.spritecollide(snake_piece, apples, False):
            snake.add(snake_piece)
            moving_piece.remove(snake_piece)
            snake_piece = Snake_Block((apple_piece.rect.x , apple_piece.rect.y))
            moving_piece.add(snake_piece)
            apples.remove(apple_piece)
            apple_piece = Apple((200 + 400*(len(snake) % 2), 100 + 200*((len(snake)+1) % 2)))
            apples.add(apple_piece)
            SCORE += 1


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                value = list(pygame.key.get_pressed()).index(1)
                if value == pygame.K_DOWN:
                    direction = directions['down']
                elif value == pygame.K_UP:
                    direction = directions['up']
                elif value == pygame.K_LEFT:
                    direction = directions['left']
                elif value == pygame.K_RIGHT:
                    direction = directions['right']


class Snake_Block(pygame.sprite.Sprite):
    def __init__(self, corr):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('J_Block.png')
        self.rect = self.image.get_rect()
        self.rect.x = corr[0]
        self.rect.y = corr[1]


class Apple(pygame.sprite.Sprite):
    def __init__(self, corr):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('O_Block.png')
        self.rect = self.image.get_rect()
        self.rect.x = corr[0]
        self.rect.y = corr[1]


def white_text_objects(text, font):
    WHITE = (255, 255, 255)
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()


def white_score_board(white_score):
    text_font = pygame.font.Font('freesansbold.ttf', 30)
    TextSurf, TextRect = white_text_objects(str(white_score), text_font)
    TextRect.center = ((400, 20))
    return TextSurf, TextRect


main()



#class Game:
    # we're going to make the board here
    # 20 by 20 matrix
    #def __init__(self):
        #self.height = 20
        #self.width = 20
        #self.correct = 'No'

    #def __repr__(self):
        #return '[]' + self.correct

    #def yes(self):
        #self.correct = 'Yes'


