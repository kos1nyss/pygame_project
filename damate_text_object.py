import pygame
from text_object import TextObject


class DamageTextObject(TextObject):
    def __init__(self, scene, size):
        super().__init__(scene, size)
        self.passed_length = 0
        self.full_color_length = 3
        self.length = 4

    def update(self, fps):
        self.update_coord(fps)
        if self.passed_length >= self.length:
            self.scene.remove(self)

    def update_coord(self, fps):
        s = -7 / fps
        self.move((0, s))
        self.passed_length += abs(s)

    def draw(self, sf):
        surface1 = pygame.Surface((self.rect.w, self.rect.h))
        surface1.set_colorkey((0, 0, 0))
        if self.passed_length >= self.full_color_length:
            surface1.set_alpha(100 - int((self.passed_length - self.full_color_length) /
                                         (self.length - self.full_color_length) * 100))
        surface1.blit(self.image, (0, 0))
        sf.blit(surface1, self.rect)
