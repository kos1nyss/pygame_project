import pygame

from math import atan2, cos, sin, radians
from random import randint, choice

from entity import Entity
from ability import Ability
from global_functions import distance
from constants import TILE_SIZE


class Shield(Ability):
    def __init__(self, scene, parent):
        super().__init__(scene, parent)
        self.r = 0
        self.max_r = 100
        self.growth_dir = 1
        self.pause = 2
        self.pause_time = 0
        self.is_growing = False

        self.power = 7
        self.pushed = []

        self.cool_down = 0.1

        self.dir_rotate = 1
        self.angle = 0
        self.rotate_speed = 100

    def draw(self, sf):
        surface1 = pygame.Surface((self.r * 2, self.r * 2))
        surface1.set_colorkey((0, 0, 0))
        surface1.set_alpha(50)
        pygame.draw.circle(surface1, (0, 153, 255), (self.r, self.r), self.r)
        n = 5
        delta_angle = int(self.angle)
        if self.is_growing or 0 < self.pause_time < self.pause:
            for angle in range(delta_angle, delta_angle + 360, 360 // n):
                pygame.draw.circle(surface1, (39, 212, 255),
                                   (cos(radians(angle)) * self.r * 0.85 + self.r,
                                    sin(radians(
                                        angle)) * self.r * 0.85 + self.r), self.r * 0.1 / 2)
        sf.blit(surface1, (self.rect.x, self.rect.y))

    def turn_on(self):
        self.dir_rotate = choice([-1, 1])
        self.angle = randint(1, 360)
        self.active = True
        self.animation_is_active = True
        self.can_turn_on = False
        self.pushed.clear()
        self.is_growing = True
        self.growth_dir = 1
        self.pause_time = 0

    def update(self, fps):
        super().update(fps)
        if self.animation_is_active:
            self.update_radius(fps)
            if self.is_growing or 0 < self.pause_time < self.pause:
                self.push()
            self.update_angle(fps)

    def update_radius(self, fps):
        if self.growth_dir == 1:
            self.r += 1000 / fps
            if self.r >= self.max_r:
                self.growth_dir = -1
                self.is_growing = False
        elif self.growth_dir == -1:
            self.pause_time += 1 / fps
            if self.pause_time >= self.pause:
                self.r -= 250 / fps
            if self.r < 0:
                self.r = 0
                self.growth_dir = 1
                self.pause_time = 0
                self.can_turn_on = False
                self.animation_is_active = False
                self.active = False
                self.cd_time = 0

    def update_angle(self, fps):
        self.angle += self.rotate_speed / fps * self.r / self.max_r * self.dir_rotate

    def push(self):
        for en in self.scene.get_objects():
            if not isinstance(en, Entity):
                continue
            if en is self.parent:
                continue
            if en not in self.pushed:
                dist = distance(self.get_coord(), en.get_coord())
                p_dist = self.r / TILE_SIZE + 0.5
                if dist < p_dist:
                    radians = atan2(en.get_coord()[1] - self.get_coord()[1]
                                    + en.rect.h / TILE_SIZE - self.parent.rect.h / TILE_SIZE,
                                    en.get_coord()[0] - self.get_coord()[0]
                                    + en.rect.w / TILE_SIZE - self.parent.rect.w / TILE_SIZE)
                    en.add_power((cos(radians) * self.power,
                                     sin(radians) * self.power - self.power * 0.3))
