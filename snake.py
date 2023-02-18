import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
# font = pygame.font.Sysfont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# RGB Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

blockSize = 20
speed = 20

class SnakeGame:

    def __init__(self, w=720, h=540):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, Point(self.head.x-blockSize, self.head.y), Point(self.head.x-(2*blockSize), self.head.y)]
        
        self.score = 0
        # self.snake = None
        self.placeFood()

    def placeFood(self):
        x = random.randint(0, (self.w-blockSize)//blockSize)*blockSize
        y = random.randint(0, (self.h-blockSize)//blockSize)*blockSize
        self.food = Point(x, y)
        if self.food in self.snake:
            self.placeFood()

    def playStep(self):
        # Collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == Direction.DOWN:
                    self.direction = Direction.DOWN

        # Move
        self._move(self.direction) # Update the head
        self.snake.insert(0, self.head) # Updates the size of the snake as the game progresses

        # Check If the game is over
        gameOver = False
        if self.isCollision():
            gameOver = True
            return gameOver, self.score

        # Place new food or jsut move
        if self.head == self.food:
            self.score += 1
            self.placeFood()
        else:
            self.snake.pop()

        # Update UI and clock
        self.updateUI()
        self.clock.tick(speed)
        # return game over and score
        return gameOver, self.score     

    def isCollision(self):
        # hits boundary
        if self.head.x > self.w - blockSize or self.head.x < 0 or self.head.y > self.h - blockSize or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True

        return False

    def updateUI(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, blockSize, blockSize))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, blockSize, blockSize))

        text = font.render('Score: ' + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += blockSize
        elif direction == Direction.LEFT:
            x -= blockSize
        elif direction == Direction.DOWN:
            y += blockSize
        elif direction == Direction.UP:
            y -= blockSize

        self.head = Point(x, y)

if __name__ == '__main__':
    game = SnakeGame()

    # Game loop
    while True:
        game_over, score = game.playStep()

        if game_over == True:
            break
    print('Final Score', score)

    pygame.quit()