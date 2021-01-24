import pygame
from random import randint
from constants import WIDTH, HEIGHT, BG_CELL_SIZE
from bg_cell import BgCell


class Background:
    def __init__(self):
        self.table = []
        self.color = pygame.Color(40, 40, 40)
        self.create()

    def create_color(self):
        color = pygame.Color(self.color.r, self.color.g, self.color.b)
        color.r = randint(self.color.r - 5, self.color.r + 5)
        color.g = randint(self.color.g - 5, self.color.g + 5)
        color.b = randint(self.color.b - 5, self.color.b + 5)
        return color

    def create(self):
        for i in range(HEIGHT // BG_CELL_SIZE + 2):
            self.table.append([])
            for j in range(WIDTH // BG_CELL_SIZE + 2):
                self.table[-1].append(
                    BgCell((j * BG_CELL_SIZE, i * BG_CELL_SIZE), self.create_color()))

    def update(self):
        self.update_table()

    def update_table(self):
        if self.table[0][0].coord[0] <= -BG_CELL_SIZE:
            for y in range(len(self.table)):
                self.table[y].append(BgCell((self.table[y][-1].coord[0] + BG_CELL_SIZE,
                                             self.table[y][0].coord[1]), self.create_color()))
                self.table[y] = self.table[y][1:]
        if self.table[0][-1].coord[0] >= WIDTH:
            for y in range(len(self.table)):
                self.table[y].insert(0, BgCell((self.table[y][0].coord[0] - BG_CELL_SIZE,
                                                self.table[y][0].coord[1]), self.create_color()))
                self.table[y] = self.table[y][:-1]
        if self.table[0][0].coord[1] <= -BG_CELL_SIZE:
            new_line = []
            for j in range(WIDTH // BG_CELL_SIZE + 2):
                new_line.append(BgCell((self.table[-1][j].coord[0],
                                        self.table[-1][0].coord[1] + BG_CELL_SIZE),
                                       self.create_color()))
            self.table.append(new_line)
            self.table = self.table[1:]
        if self.table[-1][0].coord[1] >= HEIGHT:
            new_line = []
            for j in range(WIDTH // BG_CELL_SIZE + 2):
                new_line.append(BgCell((self.table[0][j].coord[0],
                                        self.table[0][0].coord[1] - BG_CELL_SIZE),
                                       self.create_color()))
            self.table.insert(0, new_line)
            self.table = self.table[:-1]

    def move(self, delta):
        for line in self.table:
            for r in line:
                r.move(delta)

    def draw(self, sf):
        for line in self.table:
            for r in line:
                r.draw(sf)
