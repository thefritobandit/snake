class Snake(object):
    def __init__(self):
        self.body = []
        self.color = 0,0,255
        self.length = 1
        self.init_grow_to = 10
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
            sleep(1)
            sys.exit()

        elif (x, y) in self.body[1::]:
            sleep(1)
            sys.exit()

    def destroy(self):
        pass
    
    def draw(self):
        for x, y in self.body:
            pygame.draw.rect(screen, self.color, (x*grid.box, y*grid.box, self.size*grid.box, self.size*grid.box))
    
    def eat(self, length):
        self.grow_to = self.grow_to + length
        state.foodleft = state.foodleft - 1
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