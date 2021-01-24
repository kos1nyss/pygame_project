import pygame
import sys
from os import path

pygame.init()


def terminate():
    pygame.quit()
    sys.exit()


def load_image(filename, color_key=None):
    image = pygame.image.load(path.join("data", "images", filename))
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def distance(coord1, coord2):
    return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5
