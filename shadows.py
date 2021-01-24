from copy import copy
from constants import TILE_SIZE
from objects import ObjectWithSprite


class Shadow(ObjectWithSprite):
    def __init__(self, scene, coord, image):
        super().__init__(scene)
        self.coord = coord
        self.image = copy(image)
        self.alpha = self.image.get_alpha()
        self.rect = self.image.get_rect()
        self.w, self.h = self.rect.w / TILE_SIZE, self.rect.h / TILE_SIZE
        self.time = 0
        self.delta = 25

    def update(self, fps):
        self.time += 1 / fps
        if self.time >= 0.016:
            self.time = 0
            self.alpha -= self.delta
            if self.alpha < 0:
                self.scene.remove(self)
            self.image.set_alpha(self.alpha)
