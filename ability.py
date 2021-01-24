import pygame
from objects import Object


class Ability(Object):
    def __init__(self, scene, parent):
        super().__init__()
        self.set_scene(scene)
        self.active = False
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.parent = parent

        self.can_turn_on = False
        self.animation_is_active = False
        self.cool_down = 1
        self.cd_time = 0

    def update(self, fps):
        if not self.animation_is_active:
            self.update_cool_down(fps)

    def update_cool_down(self, fps):
        self.cd_time += 1 / fps
        if self.cd_time >= self.cool_down:
            self.cd_time = self.cool_down
            self.can_turn_on = True
