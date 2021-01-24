import pygame
from random import random, randint
from objects import ObjectWithPhysics
from slider_object import SliderObject
from damate_text_object import DamageTextObject
from global_functions import load_image
from constants import TILE_SIZE


class Entity(ObjectWithPhysics):
    def __init__(self, scene, game_map):
        super().__init__(scene, game_map)
        self.hp = 100

        self.rotate = 1

        self.speed_aside = 0
        self.jump_power = 0

        self.n_jumps = 2
        self.jumps_left = 0

        self.n_animation = 0
        self.animation_time = 0

        self.gun = None

        self.hp_slider = SliderObject(self.get_scene(), (0.8, 0.1))
        self.hp_slider.set_maximum(self.hp)
        self.hp_slider.set_bg_color(pygame.Color(240, 240, 240))
        self.hp_slider.set_slider_color(pygame.Color(88, 230, 60))

    def is_alive(self):
        return self.hp > 0

    def move_aside(self, direction, fps):
        if not self.is_alive(): return
        new_rotate = 1 if direction == 1 else 0
        if new_rotate != self.rotate and self.gun:
            self.gun.rotate()
        self.rotate = new_rotate
        self.move((direction * self.speed_aside / fps, 0))

    def jump(self):
        if not self.is_alive(): return
        if self.jumps_left > 0:
            self.add_power((0, -self.jump_power))
            self.jumps_left -= 1

    def add_power(self, delta):
        if not self.is_alive(): return
        super().add_power(delta)

    def update(self, fps):
        super().update(fps)
        self.update_jumps()
        if self.gun:
            self.update_gun(fps)
        self.update_ui()

    def update_jumps(self):
        if self.on_the_ground:
            self.jumps_left = self.n_jumps

    def update_gun(self, fps):
        if not self.gun:
            return
        if self.gun.animation_is_active:
            self.gun.update(fps)
        else:
            self.gun.set_coord(self.get_coord())

    def update_ui(self):
        self.hp_slider.set_coord(
            (self.get_coord()[
                 0] + self.rect.w / TILE_SIZE / 2 - self.hp_slider.rect.w / TILE_SIZE / 2,
             self.get_coord()[1] - 1.3))
        self.hp_slider.set_value(self.hp)
        if not self.is_alive():
            self.hp_slider.active = False

    def get_damage(self, damage):
        if self.hp <= damage:
            damage = self.hp
            color = pygame.Color(randint(115, 125), randint(46, 56), randint(176, 186))
        else:
            color = pygame.Color(randint(245, 255), randint(59, 79), randint(59, 79))

        text = DamageTextObject(self.scene, 20 + damage % 10)
        text.create(str(damage), color)
        x = self.get_coord()[0] - text.rect.w / 2 / TILE_SIZE + self.w / 2 + random() - 0.5
        y = self.get_coord()[1] - text.rect.h / 2 / TILE_SIZE - self.h / 2 + random() - 0.5
        text.set_coord((x, y))

        self.hp -= damage
        if self.hp <= 0:
            self.set_sprite(load_image("grave.png"))

    def delete(self):
        self.scene.remove(self.hp_slider)
        self.scene.remove(self)
        if self.gun:
            self.scene.remove(self.gun)
