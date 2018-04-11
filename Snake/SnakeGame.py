from __future__ import print_function
import sys

import curses
from random import randint
from math import *

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class SnakeGame:
    def __init__(self, board_width = 20, board_height = 20, gui = False):
        self.score = 0
        self.done = False
        self.board = {'width': board_width, 'height': board_height}
        self.gui = gui
        self.rev = 0

    def start(self):
        self.snake_init()
        self.generate_food()
        if self.gui: self.render_init()
        return self.generate_observations()

    def snake_init(self):
        x = randint(5, self.board["width"] - 5)
        y = randint(5, self.board["height"] - 5)
        self.snake = []
        vertical = randint(0,1) == 0
        if(vertical):
            self.rev = 2
        else:
            self.rev = 3
        for i in range(3):
            point = [x + i, y] if vertical else [x, y + i]
            self.snake.insert(0, point)

    def generate_food(self):
        food = []
        while food == []:
            food = [randint(1, self.board["width"]), randint(1, self.board["height"])]
            if food in self.snake: food = []
        self.food = food

    def render_init(self):
        curses.initscr()
        win = curses.newwin(self.board["width"] + 2, self.board["height"] + 2, 0, 0)
        curses.curs_set(0)
        win.nodelay(1)
        win.timeout(30)
        self.win = win
        self.render()

    def render(self):
        self.win.clear()
        self.win.border(0)
        self.win.addstr(0, 2, 'Score : ' + str(self.score) + ' ')
        self.win.addch(self.food[0], self.food[1], '🍎')
        for i, point in enumerate(self.snake):
            if i == 0:
                self.win.addch(point[0], point[1], '🔸')
            else:
                self.win.addch(point[0], point[1], '🔹')
        self.win.getch()

    def step(self, key):
        # 0 - UP
        # 1 - RIGHT
        # 2 - DOWN
        # 3 - LEFT
        if self.done == True: 
            self.end_game()
            return self.generate_observations()

        self.create_new_point(key)
        if self.food_eaten():
            self.score += 1
            self.generate_food()
        else:
            self.remove_last_point()
        self.check_collisions(key)
        if self.gui: self.render()
        return self.generate_observations()

    def create_new_point(self, key):
        new_point = [self.snake[0][0], self.snake[0][1]]
        if key == 0:
            new_point[0] -= 1
            self.rev = 2
        elif key == 1:
            new_point[1] += 1
            self.rev = 3
        elif key == 2:
            new_point[0] += 1
            self.rev = 0
        elif key == 3:
            new_point[1] -= 1
            self.rev = 1
        self.snake.insert(0, new_point)

    def remove_last_point(self):
        self.snake.pop()

    def food_eaten(self):
        return self.snake[0] == self.food

    def bad_position(self, pos, dir):
        if(abs(dir - self.rev) == 2):
            return 1

        elif(pos[0] == 0 or pos[0] == self.board["width"] + 1 or
            pos[1] == self.board["height"] + 1 or pos[1] == 0 or
            pos in self.snake[1:-1]):
            return 1
        else:
            return 0

    def is_apple(self, pos):
        return 1 if pos == self.food else 0

    def distance_apple(self, pos):
        return abs(pos[0] - self.food[0]) + abs(pos[1] - self.food[1])

    def check_collisions(self, key):
        if (self.bad_position(self.snake[0],-100)):
            self.done = True

    def generate_observations(self):
        return self.score

    def render_destroy(self):
        curses.endwin()

    def end_game(self):
        pass
    
    def generate_input(self):
        left = [self.snake[0][0], self.snake[0][1] - 1]
        right = [self.snake[0][0], self.snake[0][1] + 1]
        up = [self.snake[0][0] -1, self.snake[0][1]]
        down = [self.snake[0][0] + 1, self.snake[0][1]]

        return (self.bad_position(left,3), self.bad_position(right,1), self.bad_position(up,0), self.bad_position(down,2), 
                self.is_apple(left), self.is_apple(right), self.is_apple(up), self.is_apple(down), self.distance_apple(self.snake[0]))

if __name__ == "__main__":
    game = SnakeGame(gui = True)
    game.start()
    
    for _ in range(10000):
        x = int(input())
        eprint(game.generate_input())
        eprint(game.step(x))
        eprint(game.done)
        if(game.done): break
