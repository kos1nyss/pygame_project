import pygame
from constants import *


class Object:
    def __init__(self):
        self.active = True
        self.scene = None
        self.coord = None
        self.dx, self.dy = 0, 0

    def get_scene(self):
        return self.scene

    def set_scene(self, scene):
        self.scene = scene
        self.scene.add(self)

    def set_coord(self, coord):
        self.coord = coord

    def get_coord(self):
        return self.coord

    def move(self, delta):
        self.dx += delta[0]
        self.dy += delta[1]
        self.set_coord((self.coord[0] + delta[0], self.coord[1] + delta[1]))

    def update(self, fps):
        pass


class ObjectWithSprite(Object, pygame.sprite.Sprite):
    def __init__(self, scene):
        super().__init__()
        self.set_scene(scene)
        self.w = None
        self.h = None

    def set_sprite(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.w, self.h = self.rect.w / TILE_SIZE, self.rect.h / TILE_SIZE

    def draw(self, sf):
        sf.blit(self.image, self.rect)


class ObjectWithMove(ObjectWithSprite):
    def __init__(self, scene, game_map):
        self.w, self.h = None, None
        super().__init__(scene)
        self.game_map = game_map
        self.corners = [False for _ in range(4)]

    def move(self, delta):
        if delta[0]:
            if self.move_is_possible((delta[0], 0)):
                super().move((delta[0], 0))

        if delta[1]:
            if self.move_is_possible((0, delta[1])):
                super().move((0, delta[1]))

    def move_is_possible(self, delta):
        new_x = self.coord[0] + delta[0]
        new_y = self.coord[1] + delta[1]
        temp_corners = [False for _ in range(4)]
        for i, d in enumerate([(0, 0), (self.w, 0), (0, -self.h), (self.w, -self.h)]):
            if self.game_map.get_at((new_x + d[0], new_y + d[1])) and \
                    self.game_map.get_at((new_x + d[0], new_y + d[1])).get_collider():
                temp_corners[i] = True
                self.corners[i] = True
            else:
                temp_corners[i] = False
        if any(temp_corners):
            return False
        return True


class ObjectWithPhysics(ObjectWithMove):
    def __init__(self, scene, game_map):
        super().__init__(scene, game_map)
        self.mass = 1
        self.acceleration = [0, 0]
        self.on_the_ground = False

    def update(self, fps):
        self.update_coord(fps)
        self.update_physics(fps)

    def update_physics(self, fps):
        friction = 2
        if any(self.corners):
            friction = 4
        if self.acceleration[0] > 0:
            self.acceleration[0] -= friction / fps
            if self.acceleration[0] < 0:
                self.acceleration[0] = 0
        elif self.acceleration[0] < 0:
            self.acceleration[0] += friction / fps
            if self.acceleration[0] > 0:
                self.acceleration[0] = 0

        self.acceleration[1] += G / fps

    def update_coord(self, fps):
        self.move((self.acceleration[0] / fps, self.acceleration[1] / fps))
        if not self.move_is_possible((0, self.acceleration[1] / fps)):
            if self.acceleration[1] > 0:
                self.on_the_ground = True
            self.acceleration[1] = 0
        else:
            self.on_the_ground = False

    def add_power(self, delta):
        if delta[0]:
            self.acceleration[0] = delta[0] / self.mass
        if delta[1]:
            self.acceleration[1] = delta[1] / self.mass
