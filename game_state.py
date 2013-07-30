import pygame
from time import sleep

WIDTH = 800
HEIGHT = 700
BOX = 10
SCOREBOX_HEIGHT = 100
ROWS = (HEIGHT-SCOREBOX_HEIGHT)/BOX
COLS = WIDTH/BOX
SCREEN = pygame.display.set_mode([WIDTH,HEIGHT])

class State(object):
    def __init__(self):
        self.name = 'Guest'
        self.box = 10
        self.progression = ['levels.start', 'levels.one', 'levels.two', 'levels.three', 'levels.four', 'levels.five', 'levels.six', 'levels.gameover']
        self.level = 1
        self.active_level = self.progression[self.level]
        self.food_score = self.level * 500
        self.total_score = 0
        self.foodcount = 0
        self.pause_count = 0
        self.foodleft = 3
        self.rows = (HEIGHT-SCOREBOX_HEIGHT)/self.box
        self.cols = WIDTH/self.box
        self.score_font = pygame.font.SysFont('ledboardreversed', 30)
        self.level_label = self.score_font.render('Level: ' + str(self.level), 1, (0,0,255))
        self.food_left_label = self.score_font.render('Food Left: ' + str(self.foodleft), 1, (0,0,255))
        self.food_score_label = self.score_font.render('Food: ' + str(self.food_score), 1, (0,0,255))
        self.total_score_label = self.score_font.render('Score: ' + str(self.total_score), 1, (0,0,255))

    def drawgame_text(self):
        self.food_score_label = self.score_font.render('Food: ' + str(self.food_score), 1, (0,0,255))
        self.total_score_label = self.score_font.render('Score: ' + str(self.total_score), 1, (0,0,255))
        SCREEN.blit(self.food_score_label, (50, 650))
        SCREEN.blit(self.total_score_label, (50, 610))
        SCREEN.blit(self.level_label, (450, 610))
        SCREEN.blit(self.food_left_label, (450, 650))

    def increase_food_count(self, snake, wall):
        self.food_left_label = self.score_font.render('Food Left: ' + str(self.foodleft), 1, (0,0,255))
        self.foodcount = self.foodcount + 1
        if self.foodcount > 2:
            self.foodcount = 0
            self.next_level(snake, wall)

    def next_level(self, snake, wall):
        sleep(1.5)
        snake.grow_to = snake.init_size
        del snake.body[0:]
        snake.x = COLS/2
        snake.y = ROWS/2
        snake.turn('up', 'down')
        self.foodleft = 3
        self.level = self.level + 1
        self.food_left_label = self.score_font.render('Food Left: ' + str(self.foodleft), 1, (0,0,255))
        self.level_label = self.score_font.render('Level: ' + str(self.level), 1, (0,0,255))
        wall.create_level(self.level)
        self.pause_count = 0
        
    def score_adjust(self):
        if self.food_score > 0:
            self.food_score = int(self.food_score - (2 * self.level))
        else:
            self.food_score = 0
        
    def score_reset(self):
        self.total_score = self.total_score + self.food_score
        self.food_score = .5 * self.level * 1000
