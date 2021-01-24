import pygame
from random import randint
from constants import BG_CELL_SIZE


class BgCell:
    def __init__(self, coord, color):
        self.coord = list(coord)
        self.color = color

    def move(self, delta):
        self.coord[0] += delta[0]
        self.coord[1] += delta[1]

    def draw(self, sf):
        pygame.draw.rect(sf, self.color, (*self.coord, BG_CELL_SIZE, BG_CELL_SIZE))
