import pygame
from global_functions import distance
from constants import TILE_SIZE
from enemy import Enemy
from random import randint
from bluecube_images import *
from guns import *


class BlueCubeEnemy(Enemy):
    def __init__(self, scene, game_map):
        self.hp = 50
        super().__init__(scene, game_map)
        self.image = pygame.Surface((64, 64))
        self.image.fill(pygame.Color(randint(15, 35), randint(15, 35), randint(92, 112)))
        self.rect = self.image.get_rect()
        self.w, self.h = self.rect.w / TILE_SIZE, self.rect.h / TILE_SIZE

        self.speed_aside = 3
        self.jump_power = 10
        self.gun = BlueSword(self.scene, self)

    def update(self, fps):
        super().update(fps)
        if self.gun and self.is_alive():
            self.update_gun(fps)
        if self.is_alive():
            self.update_animation(fps)
            if self.gun:
                self.update_gun(fps)

    def update_gun(self, fps):
        if not self.target:
            return
        if not self.target.is_alive():
            return
        if self.gun.animation_is_active:
            return
        if distance(self.get_coord(), self.target.get_coord()) >= 2:
            return
        self.gun.punch()

    def update_animation(self, fps):
        if not self.is_alive(): return
        if self.dx == 0:
            animation_step_time = 0.8
            self.n_animation %= len(stand_animations[self.rotate])
            self.set_sprite(stand_animations[self.rotate][self.n_animation])
        else:
            animation_step_time = 0.3
            self.n_animation %= len(run_animations[self.rotate])
            self.set_sprite(run_animations[self.rotate][self.n_animation])

        self.animation_time += 1 / fps
        if self.animation_time >= animation_step_time:
            self.animation_time = 0
            self.n_animation += 1
