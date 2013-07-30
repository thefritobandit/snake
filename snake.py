import os
import pygame
import sys
from time import sleep
from game_objects import Food, Level, Snake
from game_state import BOX, SCREEN, State

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
clock = pygame.time.Clock()
fps = 30
PAUSE_COUNT = 0

def check(foodx, foody, wall):
    x, y = snake.body[0]
    if x == foodx and y == foody:
         snake.eat(food.get_eaten(wall.wall), state, wall)

    elif (x, y) in wall.wall:
        sleep(1)
        sys.exit()

    elif (x, y) in snake.body[1:]:
        sleep(1)
        sys.exit()

def draw_game():
    snake.move()
    wall.draw()
    food.draw()
    snake.draw()
    state.drawgame_text()

def event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_LEFT:
                snake.turn('left', 'right')
            elif event.key == pygame.K_RIGHT:
                snake.turn('right', 'left')
            elif event.key == pygame.K_UP:
                snake.turn('up', 'down')
            elif event.key == pygame.K_DOWN:
                snake.turn('down', 'up')

def level_actions():
    global  PAUSE_COUNT
    if PAUSE_COUNT == 0:
        pygame.display.flip()
        sleep(1.5)
        PAUSE_COUNT = PAUSE_COUNT + 1
    check(food.x, food.y, wall)
    state.score_adjust()

state = State()
snake = Snake()
wall = Level()
wall.create_level(state.level)
food = Food()
food.check(food.x, food.y, wall.wall)

while __name__ == '__main__':
    tickFPS = clock.tick(fps)
    pygame.display.set_caption("Press Esc to quit. FPS: %.2f" % (clock.get_fps()))
    SCREEN.fill((0,0,0))
    event_handler()
    draw_game()
    level_actions()
    pygame.display.flip()
