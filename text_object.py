import pygame
from ui_object import UiObject
from os import path


class TextObject(UiObject):
    def __init__(self, scene, size):
        super().__init__(scene)

        self.size = size
        self.font = pygame.font.Font(path.join("data", "fonts", "kongtext.ttf"), size)

        self.rect = pygame.Rect(0, 0, 0, 0)

    def create(self, text, color):
        self.image = self.font.render(text, False, color)
        self.rect = self.image.get_rect()
