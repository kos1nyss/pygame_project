import pygame
from global_functions import distance
from math import floor, atan2, cos, sin
from constants import *
from entity import Entity
from random import randint


class Enemy(Entity):
    def __init__(self, scene, game_map):
        super().__init__(scene, game_map)
        self.chunk_n = None
        self.target = None

        self.speed_aside = 0
        self.jump_power = 0

    def update(self, fps):
        super().update(fps)
        if self.target and self.target.is_alive():
            self.move_to_target(fps)
        self.update_chunk()

    def update_chunk(self):
        new_chunk_n = floor(self.coord[0]) // 20, floor(self.coord[1]) // 20
        if not self.chunk_n:
            self.chunk_n = new_chunk_n
            return

        if new_chunk_n != self.chunk_n:
            self.game_map.chunks[self.chunk_n].delete_enemy(self)
            if new_chunk_n in self.game_map.chunks:
                self.game_map.chunks[new_chunk_n].add_enemy(self)
                self.chunk_n = new_chunk_n
            else:
                self.delete()

    def update_target(self, player):
        if distance(self.get_coord(), player.get_coord()) < 5:
            self.target = player
        else:
            self.target = None

    def move_to_target(self, fps):
            rad = atan2(self.target.get_coord()[1] - self.get_coord()[1],
                        self.target.get_coord()[0] - self.get_coord()[0])
            if abs(self.get_coord()[0] - self.target.get_coord()[0]) > 0.1:
                self.move_aside(1 if cos(rad) > 0 else -1, fps)
            if self.dy >= 0 and sin(rad) < -0.5:
                self.jump()
