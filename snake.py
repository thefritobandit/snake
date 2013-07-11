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
    def __init__(self):
        self.box = 10
        self.rows = height/self.box
        self.cols = width/self.box
        self.layout = [[(j, i) for i in xrange(self.rows)] for j in xrange(self.cols)]

class Snake(object):
    def __init__(self):
        self.body = []
        self.color = 0,0,255
        self.length = 1
        self.grow_to = 5
        self.size = 1
        self.x = grid.cols/2
        self.y = grid.rows/2
        self.speed = 1
        self.vx = 0
        self.vy = -self.speed
        self.direction = 'up'

    def check(self):
        x, y = self.body[0]
        if x == food.x and y == food.y:
            self.eat(food.get_eaten())
        
        elif (x, y) in wall.wall:
            sys.quit()
    
    def destroy(self):
        pass
    
    def draw(self):
        for x, y in self.body:
            pygame.draw.rect(screen, self.color, (x*grid.box, y*grid.box, self.size*grid.box, self.size*grid.box))
    
    def eat(self, length):
        self.grow_to = self.grow_to + length
    
    def move(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        x, y = grid.layout[self.x][self.y]

        self.body.insert(0, (x, y))
        
        self.length = len(self.body)
        
        if self.length > self.grow_to:
            self.body.pop()
    
    def speedup(self, acceleration):
        self.speed = self.speed + acceleration
        
    def turn(self, turn, oturn):
        if turn != self.direction and oturn != self.direction:
            self.direction = turn
        
        if self.direction == 'up':
            self.vx = 0
            self.vy = -self.speed

        elif self.direction == 'down':
            self.vx = 0
            self.vy = self.speed

        elif self.direction == 'left':
            self.vx = -self.speed
            self.vy = 0

        elif self.direction == 'right':
            self.vx = self.speed
            self.vy = 0
    
class Food(object):
    def __init__(self):
        self.color = 255,0,0
        self.size = 1
        self.grow_value = 5
        self.location = grid.layout[randint(grid.box, grid.cols-2)][randint(grid.box, grid.rows-2)]
        self.x, self.y = self.location

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x*grid.box, self.y*grid.box, self.size*grid.box, self.size*grid.box))

    def get_eaten(self):
        self.x, self.y = self.location
        return self.grow_value

class Wall(object):
    def __init__(self):
        self.color = 255,102,0
        self.size = 1
        self.x = 0
        self.y = 0
        self.wall = []

    def destroy(self):
        pass
    
    def draw(self):
        self.wall = []
        for i in xrange(grid.cols):
            for j in xrange(grid.rows):
                self.x, self.y = grid.layout[i][j]
                if self.x == 0 or self.y == 0 or self.x == grid.cols-1 or self.y == grid.rows-1:
                    self.wall.append((self.x, self.y))
                    pygame.draw.rect(screen, self.color, (self.x*grid.box, self.y*grid.box, self.size*grid.box, self.size*grid.box))

grid = Grid()
snake = Snake()
food = Food()
wall = Wall()

while __name__ == '__main__':
    tickFPS = clock.tick(fps)
    pygame.display.set_caption("Press Esc to quit. FPS: %.2f" % (clock.get_fps()))
    screen.fill((0,0,0))
    event_handler()
    food.draw()
    snake.draw()
    wall.draw()
    snake.move()
    snake.check()
    pygame.display.flip()
