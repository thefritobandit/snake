import os
from game_objects import *
from game_state import *
import levels
import pygame
from random import randint
import sys
from time import sleep

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
width = 800
height = 700
scorebox_height = 100
screen = pygame.display.set_mode([width,height])
clock = pygame.time.Clock()
fps = 30

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

class Grid(object):
    def __init__(self):
        self.box = 10
        self.rows = (height-scorebox_height)/self.box
        self.cols = width/self.box
        self.layout = [[(j, i) for i in xrange(self.rows)] for j in xrange(self.cols)]

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
            pygame.draw.rect(screen, self.color, (self.x*grid.box, self.y*grid.box, self.size*grid.box, self.size*grid.box))

state = State()
grid = Grid()
snake = Snake()
wall = Level()
wall.create_level(state.level)
food = Food()
food.check(food.x, food.y)

while __name__ == '__main__':
    tickFPS = clock.tick(fps)
    pygame.display.set_caption("Press Esc to quit. FPS: %.2f" % (clock.get_fps()))
    screen.fill((0,0,0))
    event_handler()
    state.draw_game()
    state.level_actions()
    pygame.display.flip()
