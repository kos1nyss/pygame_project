import pygame
from shadows import *
from player_images import *
from entity import Entity
from slider_object import SliderObject
from guns import Sword


class Player(Entity):
    def __init__(self, scene, game_map):
        super().__init__(scene, game_map)
        self.set_sprite(stand_animations[0][0])
        self.shadow_time = 0

        self.ability = None
        self.ability_cd_slider = None

        self.gun = Sword(self.scene, self)

        self.speed_aside = 7
        self.jump_power = 15

    def set_ability(self, ability):
        self.ability = ability
        self.make_ability_slider()

    def make_ability_slider(self):
        self.ability_cd_slider = SliderObject(self.get_scene(), (0.8, 0.1))
        self.ability_cd_slider.set_maximum(self.ability.cool_down)
        self.ability_cd_slider.set_bg_color(pygame.Color(240, 240, 240))
        self.ability_cd_slider.set_slider_color(pygame.Color(45, 155, 235))

    def use_ability(self):
        if not self.is_alive():
            return
        if not self.ability:
            return
        if not self.ability.can_turn_on:
            return
        self.ability.turn_on()

    def update(self, fps):
        super().update(fps)
        self.update_shadow(fps)
        if self.ability:
            self.update_ability_pos()
        self.update_animation(fps)

    def update_animation(self, fps):
        if not self.is_alive(): return
        if self.dy != 0:
            animation_step_time = 0.3
            self.n_animation %= len(jump_animations[self.rotate])
            self.set_sprite(jump_animations[self.rotate][self.n_animation])
        else:
            if self.dx == 0:
                animation_step_time = 0.5
                self.n_animation %= len(stand_animations[self.rotate])
                self.set_sprite(stand_animations[self.rotate][self.n_animation])
            else:
                animation_step_time = 0.1
                self.n_animation %= len(run_animations[self.rotate])
                self.set_sprite(run_animations[self.rotate][self.n_animation])

        self.animation_time += 1 / fps
        if self.animation_time >= animation_step_time:
            self.animation_time = 0
            self.n_animation += 1

    def update_shadow(self, fps):
        self.shadow_time += 1 / fps
        if self.shadow_time >= 0.075:
            self.shadow_time = 0
            Shadow(self.scene, self.get_coord(), self.image)

    def update_ability_pos(self):
        self.ability.set_coord(self.get_coord())

    def update_ui(self):
        if not self.is_alive():
            return
        if self.ability:
            if self.ability.animation_is_active:
                self.ability_cd_slider.active = False
                self.hp_slider.active = False
            else:
                self.ability_cd_slider.active = True
                self.hp_slider.active = True
                self.ability_cd_slider.set_coord(
                    (self.get_coord()[
                         0] + self.rect.w / TILE_SIZE / 2 - self.ability_cd_slider.rect.w / TILE_SIZE / 2,
                     self.get_coord()[1] - 1.4))
                self.ability_cd_slider.set_value(self.ability.cd_time)
        super().update_ui()
