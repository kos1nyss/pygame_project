from objects import ObjectWithSprite
from random import randint


class Gun(ObjectWithSprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.damage = 0

    def get_damage(self):
        return randint(max(self.damage - 10, 1), self.damage + 10)
