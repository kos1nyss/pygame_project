import pygame
from entity import Entity
from math import sin, cos, radians, atan2, pi
from random import choice
from constants import TILE_SIZE
from gun import Gun

from global_functions import load_image, distance


class MeleeGun(Gun):
    def __init__(self, scene, parent):
        self.parent = parent
        super().__init__(scene)
        self.set_coord((0, 0))
        self.power = 0

        self.active = False
        self.animation_is_active = False
        self.source_image = None
        self.delta_rotate = -180
        self.rotate_speed = None
        self.r = None
        self.min_angle = None
        self.max_angle = None
        self.delta_angle = None
        self.dir = 1
        self.prev_angle = 0
        self.angle = 0
        self.damage = 0
        self.damaged = []

    def set_image(self, image):
        self.source_image = image
        self.rect = self.source_image.get_rect()

    def set_angles(self, mn, mx):
        self.min_angle = mn
        self.max_angle = mx
        self.angle = self.min_angle

    def update(self, fps):
        if not self.parent.is_alive():
            return
        self.active = self.animation_is_active
        if self.animation_is_active:
            self.update_angle(fps)
            self.update_image()
            self.update_coord()
            self.make_damage()

    def update_angle(self, fps):
        self.prev_angle = self.angle
        self.angle += self.rotate_speed * 1 / fps * self.dir
        if self.dir == 1:
            if self.angle >= self.max_angle:
                self.angle = self.max_angle
                self.prev_angle = self.angle
                self.dir = -self.dir
                self.animation_is_active = False
        elif self.dir == -1:
            if self.angle <= self.min_angle:
                self.angle = self.min_angle
                self.prev_angle = self.angle
                self.dir = -self.dir
                self.animation_is_active = False

    def update_image(self):
        self.image = pygame.transform.rotate(self.source_image, -self.angle - 90)
        self.rect = self.image.get_rect()

    def update_coord(self):
        self.set_coord(self.parent.get_coord())
        x = self.get_coord()[0] + cos(radians(self.angle)) * self.r
        y = self.get_coord()[1] + sin(radians(self.angle)) * self.r
        self.set_coord((x, y))

    def punch(self):
        self.damaged = []
        self.animation_is_active = True

    def rotate(self):
        if self.dir == 1:
            self.angle = self.max_angle
        elif self.dir == -1:
            self.angle = self.min_angle
        self.dir = -self.dir

        self.prev_angle += self.delta_rotate
        self.angle += self.delta_rotate
        self.min_angle += self.delta_rotate
        self.max_angle += self.delta_rotate
        self.delta_rotate = -self.delta_rotate

    def make_damage(self):
        for en in self.scene.get_objects():
            if not isinstance(en, Entity):
                continue
            if not en.is_alive():
                continue
            if en is self.parent:
                continue
            if en in self.damaged:
                continue
            segments = 5
            for i in range(segments):
                r = (self.r + self.source_image.get_size()[1] / TILE_SIZE / 1.5) * i / segments
                x = self.parent.get_coord()[0] + self.parent.w / 2 + cos(self.angle) * r
                y = self.parent.get_coord()[1] - self.parent.h / 2 + sin(self.angle) * r
                if en.get_coord()[0] <= x <= en.get_coord()[0] + en.w and \
                        en.get_coord()[1] - en.h <= y <= en.get_coord()[1]:
                    en.add_power((cos(self.angle) * self.power, sin(self.angle) * self.power - 2))
                    en.get_damage(self.get_damage())
                    if not en.is_alive():
                        self.parent.add_kill()
                    self.damaged.append(en)
                    break
