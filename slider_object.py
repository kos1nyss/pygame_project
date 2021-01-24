import pygame
from constants import TILE_SIZE
from ui_object import UiObject


class SliderObject(UiObject):
    def __init__(self, scene, size):
        super().__init__(scene)

        self.size = size
        self.mx = None
        self.value = None

        self.set_size(size)
        self.make_surface()

        self.slider_color = None
        self.bg_color = None

    def make_surface(self):
        self.image = pygame.Surface((self.size[0] * TILE_SIZE, self.size[1] * TILE_SIZE))
        self.rect = self.image.get_rect()

    def set_size(self, size):
        self.size = size

    def set_maximum(self, mx):
        self.mx = mx

    def set_value(self, value):
        if value > self.mx:
            value = self.mx
        self.value = value

    def set_slider_color(self, c):
        self.slider_color = c

    def set_bg_color(self, c):
        self.bg_color = c

    def draw(self, sf):
        try:
            self.image.fill(self.bg_color)
            pygame.draw.rect(self.image, self.slider_color,
                             (0, 0, self.rect.w * self.value / self.mx, self.rect.h))
            sf.blit(self.image, self.rect)
        except Exception:
            pass
