import pygame
from copy import deepcopy
from itertools import product as cmb
import sys

BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
RED = pygame.Color('red')
GREEN = pygame.Color('green')


def pointInRect(point, rect):
    x1, y1, w, h = rect
    x2, y2 = x1 + w, y1 + h
    x, y = point
    if x1 < x < x2:
        if y1 < y < y2:
            return True
    return False


class Board:
    def __init__(self, width, height):
        self.current = True
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def get_cell(self, pos):
        for x in range(self.height):
            for y in range(self.width):
                if pointInRect(pos, (x * self.cell_size + self.left,
                                     y * self.cell_size + self.top,
                                     self.cell_size, self.cell_size)):
                    return x, y
        return None

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def on_click(self, cell):
        pass

    def render(self):
        c = self.cell_size
        for x in range(self.height):
            for y in range(self.width):
                pos = (x * c + self.left, y * c + self.top, c, c)
                pygame.draw.rect(screen, WHITE, pos, 1)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size


class GameOfLife(Board):
    def __init__(self):
        super(GameOfLife, self).__init__(26, 26)
        self.drawing = False

    def on_click(self, cell):
        if not cell:
            return
        x, y = cell
        if not self.drawing:
            self.board[x][y] = (self.board[x][y] + 1) % 2

    def get_neighbours(self, x, y):
        def get(r, c):
            return self.board[r % self.height][c % self.width]
        return sum(get(x + i, y + j) for i, j in cmb(range(-1, 2), range(-1, 2)) if i or j)

    def get_next_generation(self):
        tmp = deepcopy(self.board)
        for x in range(self.height):
            for y in range(self.width):
                alive = self.get_neighbours(x, y)
                if self.board[x][y]:
                    if alive in (2, 3):
                        tmp[x][y] = 1
                    else:
                        tmp[x][y] = 0
                else:
                    if alive == 3:
                        tmp[x][y] = 1
                    else:
                        tmp[x][y] = 0
        self.board[:] = tmp

    def render(self):
        super(GameOfLife, self).render()
        c = self.cell_size
        if self.drawing:
            self.get_next_generation()
        for x in range(self.height):
            for y in range(self.width):
                pos = x * c + self.left, y * c + self.top, c, c
                if self.board[x][y]:
                    pygame.draw.rect(screen, GREEN, pos)


board = GameOfLife()
pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(int(event.key)) == 'space':
                board.drawing = not board.drawing
    screen.fill(BLACK)
    board.render()
    pygame.display.flip()
    clock.tick(10)
