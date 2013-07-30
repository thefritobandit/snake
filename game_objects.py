from game_state import BOX, COLS, ROWS, SCREEN
import levels
from random import randint
import pygame
from time import sleep

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

class Snake(object):
    def __init__(self):
        # reset values
        self.init_size = 10
        self.initx = COLS/2
        self.inity = ROWS/2
        
        # grow values        
        self.grow_to = 15
        self.size = 1
        
        # movement values        
        self.x = self.initx
        self.y = self.inity
        self.speed = 1
        self.vx = 0
        self.vy = -self.speed
        self.turn('up', 'down')

        # snake body values
        self.body = []
        self.color = 0,0,255
        self.length = 1

    def draw(self):
        for x, y in self.body:
            pygame.draw.rect(SCREEN, self.color, (x*BOX, y*BOX, self.size*BOX, self.size*BOX))
    
    def eat(self, amount, state, wall):
        self.grow(amount)
        state.foodleft = state.foodleft - 1
        state.score_reset()
        state.increase_food_count(self, wall)

    def grow(self, amount):
        self.grow_to = self.grow_to + amount
    
    def move(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        x, y = self.x, self.y

        self.body.insert(0, (x, y))
        
        length = len(self.body)
        
        if length > self.grow_to:
            self.body.pop()
        
    def turn(self, turn, oturn):
        # don't go back on self; would be insta-death
        if turn == oturn:
            pass
        
        elif turn == 'up':
            self.vx = 0
            self.vy = -self.speed

        elif turn == 'down':
            self.vx = 0
            self.vy = self.speed

        elif turn == 'left':
            self.vx = -self.speed
            self.vy = 0

        elif turn == 'right':
            self.vx = self.speed
            self.vy = 0
    
class Food(object):
    def __init__(self):
        self.color = 255,0,0
        self.size = 1
        self.grow_value = 10
        self.speed_value = 1
        self.eaten_counter = 0
        self.x, self.y = (randint(1, COLS-2)), (randint(1, ROWS-2))

    def check(self, x, y, wall):
        if (x, y) in wall:
            self.x, self.y = (randint(1, COLS-2)), (randint(1, ROWS-2))
            self.check(self.x, self.y)

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, (self.x*BOX, self.y*BOX, self.size*BOX, self.size*BOX))

    def get_eaten(self, wall):
        self.x, self.y = (randint(1, COLS-2)), (randint(1, ROWS-2))
        self.check(self.x, self.y, wall)
        return self.grow_value
