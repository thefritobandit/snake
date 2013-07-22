import os
import levels
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

class State(object):
    def __init__(self):
        self.score = 0
        self.name = 'Guest'
        self.progression = ['levels.start', 'levels.one', 'levels.two', 'levels.three', 'levels.four', 'levels.five', 'levels.gameover']
        self.level = 0
        self.active_level = self.progression[self.level]

    def next_level(self):
        self.level = self.level + 1
        

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
            sys.exit()

        elif (x, y) in self.body[1::]:
            sys.exit()

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
        self.speed_value = 1
        self.eaten_counter = 0
        self.x, self.y = (randint(1, grid.cols-2)), (randint(1, grid.rows-2))

    def check(self, x, y):
        if (x, y) in wall.wall:
            self.x, self.y = (randint(1, grid.cols-2)), (randint(1, grid.rows-2))
            self.check(self.x, self.y)

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x*grid.box, self.y*grid.box, self.size*grid.box, self.size*grid.box))

    def get_eaten(self):
        self.x, self.y = (randint(1, grid.cols-2)), (randint(1, grid.rows-2))
        self.check(self.x, self.y)
        return self.grow_value

class Level(object):
    def __init__(self):
        self.size = 1
        self.color = 255,120,0
        self.x = 0
        self.y = 0
        self.layout = []
        self.wall = []
        
    def create_level(self, level):
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

        for i in xrange(len(self.layout)):
            for j in xrange(len(self.layout[0])):
                if self.layout[i][j] == 1:
                    self.wall.append((j, i))

    def draw(self):
        for self.x, self.y in self.wall:
            pygame.draw.rect(screen, self.color, (self.x*grid.box, self.y*grid.box, self.size*grid.box, self.size*grid.box))

grid = Grid()
snake = Snake()
wall = Level()
wall.create_level(5)
food = Food()
food.check(food.x, food.y)

while __name__ == '__main__':
    tickFPS = clock.tick(fps)
    pygame.display.set_caption("Press Esc to quit. FPS: %.2f" % (clock.get_fps()))
    screen.fill((0,0,0))
    event_handler()
    snake.move()
    wall.draw()
    food.draw()
    snake.draw()
    snake.check()
    pygame.display.flip()
