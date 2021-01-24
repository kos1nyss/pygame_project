import pygame
from random import randint
from constants import *
from images import stone_image, block_outline, wood_image
from objects import *
from execeptions import *


class Tile(ObjectWithSprite):
    def __init__(self, scene, coord):
        super().__init__(scene)
        self.set_coord(coord)

    def is_on_the_cell(self):
        return -TILE_SIZE < self.rect.x < WIDTH and -TILE_SIZE < self.rect.y < HEIGHT

    def get_collider(self):
        return self.collider

    def set_coord(self, coord):
        if coord[0] != coord[0] // 1 or coord[1] != coord[1] // 1:
            raise TileCoordinateError
        super().set_coord(coord)


class EmptyTile(Tile):
    def __init__(self, scene, coord):
        self.collider = 0
        super().__init__(scene, coord)
        self.rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)

    def draw(self, sf):
        pass


class BorderTile(Tile):
    def __init__(self, scene, coord):
        self.collider = True
        super().__init__(scene, coord)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill("grey")
        self.rect = self.image.get_rect()


class StoneBorderTile(BorderTile):
    def __init__(self, scene, coord):
        self.collider = True
        super().__init__(scene, coord)
        self.image = stone_image
        self.rect = self.image.get_rect()


class WoodBorderTile(BorderTile):
    def __init__(self, scene, coord):
        self.collider = True
        super().__init__(scene, coord)
        self.image = wood_image
        self.rect = self.image.get_rect()


class RandomBorderTile(Tile):
    def __init__(self, scene, coord):
        self.collider = True
        self.can_update = True
        super().__init__(scene, coord)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.update_image()

    def update(self, fps):
        if not self.can_update and self.is_on_the_cell():
            self.can_update = True
        elif self.can_update and not self.is_on_the_cell():
            self.can_update = False
            self.update_image()

    def update_image(self):
        self.image.fill(pygame.Color(randint(50, 255), randint(50, 255), randint(50, 255)))
        outline = block_outline
        self.image.blit(outline, (0, 0))
        self.rect = self.image.get_rect()


class BlackBorderTIle(Tile):
    def __init__(self, scene, coord):
        self.collider = True
        super().__init__(scene, coord)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(pygame.Color(51, 51, 51))
        outline = block_outline
        self.image.blit(outline, (0, 0))
        self.rect = self.image.get_rect()
