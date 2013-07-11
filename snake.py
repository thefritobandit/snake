import os
import pygame
from random import randint
import sys

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
width = 800
height = 600
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
    self.box = 10
    self.rows = height/self.box
    self.cols = width/self.box
    self.layout = [[(i, j) for i in cols] for j in rows]

class Snake(object):
    def __init__(self):
        self.body = []
        self.color = 0,0,255
        self.grow_to = 3
        self.size = 1
        self.x = width/2
        self.y = height/2
        self.speed = 1
        self.vx = 0
        self.vy = -self.speed
    
    def destroy(self):
        pass
    
    def draw(self):
        pass
    
    def eat(self):
        pass
            
    def grow(self):
        pass
    
    def move(self):
        pass
    
    def speedup(self, acceleration):
        pass
        
    def turn(self, turn, oturn):
        pass
            
class Food(object):
    def __init__(self):
        self.color = 255,0,0
        self.size = 10
        self.x = randint(0, width)
        self.y = randint(0, height)

    def draw(self):
        pass

    def get_eaten(self):
        pass

class Wall(object):
    def __init__(self):
        self.color = 255,102,0
        self.size = 10
        self.x = 0
        self.y = 0

    def destroy(self):
        pass
    
    def draw(self):
        pass

grid = Grid()
snake = Snake()
food = Food()

while __name__ == '__main__':
    tickFPS = clock.tick(fps)
    pygame.display.set_caption("Press Esc to quit. FPS: %.2f" % (clock.get_fps()))
    screen.fill((0,0,0))
    event_handler()
    snake.draw()
    snake.move()
    pygame.display.flip()
