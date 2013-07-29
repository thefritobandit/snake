import os
import levels
import pygame
import sys
from time import sleep
from game_objects import *
from game_state import BOX, SCREEN, State

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
clock = pygame.time.Clock()
fps = 30
PAUSE_COUNT = 0

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
    if PAUSE_COUNT == 0:
        pygame.display.flip()
        sleep(1.5)
        PAUSE_COUNT = PAUSE_COUNT + 1
    snake.check()
    state.score_adjust()

#===============================================================================
# class Grid(object):
#     def __init__(self):
#         self.BOX = 10
#         self.rows = (height-scorebox_height)/self.BOX
#         self.cols = width/self.BOX
#         self.layout = [[(j, i) for i in xrange(self.rows)] for j in xrange(self.cols)]
#===============================================================================

class Level(object):
    def __init__(self):
        self.size = 1
        self.color = 255,120,0
        self.x = 0
        self.y = 0
        self.layout = []
        self.wall = []
        
    def create_level(self, level):
        self.wall = []
        if level == 1:
            self.layout = levels.one
        elif level == 2:
            self.layout = levels.two
        elif level == 3:
            self.layout = levels.three
        elif level == 4:
            self.layout = levels.four
        elif level == 5:
            self.layout = levels.five
        elif level == 6:
            self.layout = levels.six

        for i in xrange(len(self.layout)):
            for j in xrange(len(self.layout[0])):
                if self.layout[i][j] == 1:
                    self.wall.append((j, i))

    def draw(self):
        for self.x, self.y in self.wall:
            pygame.draw.rect(SCREEN, self.color, (self.x*BOX, self.y*BOX, self.size*BOX, self.size*BOX))

state = State()
#----------------------------------------------------------------- grid = Grid()
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
