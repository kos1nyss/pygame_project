import pygame
from text import Text
from constants import SIZE, WIDTH, HEIGHT


class Pause:
    def __init__(self):
        self.active = False

        self.image = None
        self.make_image()

    def switch(self):
        self.active = not self.active

    def make_image(self):
        self.image = pygame.Surface(SIZE)
        self.image.set_colorkey((0, 0, 0))
        self.image.set_alpha(30)

        self.image.fill("white")
        text = Text(50)
        text.create("PAUSE", (WIDTH // 10, HEIGHT // 10), "black")
        text.draw(self.image)

    def draw(self, sf):
        sf.blit(self.image, (0, 0))

    def get_active(self):
        return self.active
