import pygame
from os import path


class Text:
    def __init__(self, size):
        self.text_image = None
        self.rect_image = None
        self.font = pygame.font.Font(path.join("data", "fonts", "kongtext.ttf"), size)

    def create(self, text, coord, color):
        self.text_image = self.font.render(text, False, color)
        self.rect_image = self.text_image.get_rect(topleft=coord)

    def draw(self, sf):
        sf.blit(self.text_image, self.rect_image)
