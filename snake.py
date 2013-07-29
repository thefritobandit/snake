import os
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

class State(object):
    def __init__(self):
        self.name = 'Guest'
        self.progression = ['levels.start', 'levels.one', 'levels.two', 'levels.three', 'levels.four', 'levels.five', 'levels.six', 'levels.gameover']
        self.level = 1
        self.active_level = self.progression[self.level]
        self.food_score = self.level * 500
        self.total_score = 0
        self.foodcount = 0
        self.score_font = pygame.font.SysFont('ledboardreversed', 30)
        self.level_label = self.score_font.render('Level: ' + str(self.level), 1, (0,0,255))
        self.food_score_label = self.score_font.render('Food: ' + str(self.food_score), 1, (0,0,255))
        self.total_score_label = self.score_font.render('Score: ' + str(self.total_score), 1, (0,0,255))

    def draw_game(self):
        snake.move()
        wall.draw()
        food.draw()
        snake.draw()
        state.drawgame_text()

    def drawgame_text(self):
        self.food_score_label = self.score_font.render('Food: ' + str(self.food_score), 1, (0,0,255))
        self.total_score_label = self.score_font.render('Score: ' + str(self.total_score), 1, (0,0,255))
        screen.blit(self.food_score_label, (50, 650))
        screen.blit(self.total_score_label, (50, 610))
        screen.blit(state.level_label, (550, 610))

    def increase_food_count(self):
        self.foodcount = self.foodcount + 1
        if self.foodcount > 9:
            self.foodcount = 0
            self.next_level()
        
    def next_level(self):
        self.level = self.level + 1
        
    def score_adjust(self):
        if self.food_score > 0:
            self.food_score = int(self.food_score - (2 * self.level))
        else:
            self.food_score = 0
        
    def score_reset(self):
        self.total_score = self.total_score + self.food_score
        self.food_score = .5 * self.level * 1000

class Grid(object):
    def __init__(self):
        self.box = 10
        self.rows = (height-scorebox_height)/self.box
        self.cols = width/self.box
        self.layout = [[(j, i) for i in xrange(self.rows)] for j in xrange(self.cols)]

class Snake(object):
    def __init__(self):
        self.body = []
        self.color = 0,0,255
        self.length = 1
        self.grow_to = 15
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
        state.score_reset()
        state.increase_food_count()
        
    
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
        self.grow_value = 10
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
    snake.check()
    state.score_adjust()
    pygame.display.flip()
