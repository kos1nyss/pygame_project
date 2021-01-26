import pygame
from objects import Object
from tiles import *
from constants import *
from blue_cube_enemy import *
from chunks import chunks
from random import choice
from guns import Sword


class Chunk(Object):
    tile_from_character = {"#": StoneBorderTile,
                           "$": RandomBorderTile,
                           "%": BlackBorderTIle,
                           "&": WoodBorderTile}

    def __init__(self, scene, coord, game_map):
        super().__init__()
        self.game_map = game_map
        self.start_player_pos = 0, 0
        self.set_scene(scene)
        self.set_coord(coord)
        self.matrix = choice(chunks)
        self.tiles = []
        self.enemies = []
        self.form_matrix_to_tiles()

    def get_start_player_pos(self):
        return self.coord[0] + self.start_player_pos[0], \
               self.coord[1] + self.start_player_pos[1]

    def form_matrix_to_tiles(self):
        en_pos = []
        for y, line in enumerate(self.matrix):
            self.tiles.append([])
            for x, c in enumerate(line):
                coord = self.coord[0] + x, self.coord[1] + y
                if c == " ":
                    self.tiles[-1].append(None)
                    continue
                elif c == "P":
                    self.tiles[-1].append(None)
                    self.start_player_pos = x, y
                    continue
                elif c == "E":
                    self.tiles[-1].append(None)
                    en_pos.append(coord)
                else:
                    new_tile = Chunk.tile_from_character[c](self.scene, coord)
                    self.tiles[-1].append(new_tile)
        e = randint(2, len(en_pos))
        while e:
            new_enemy = BlueCubeEnemy(self.get_scene(), self.game_map)
            new_enemy.set_coord(en_pos.pop())
            self.enemies.append(new_enemy)
            e -= 1

    def delete(self):
        for line in self.tiles:
            for block in line:
                if block:
                    self.scene.remove(block)
        for enemy in self.enemies:
            enemy.delete()

    def is_on_the_cell(self):
        for line in self.tiles:
            for block in line:
                if block and block.is_on_the_cell():
                    return True
        return False

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def delete_enemy(self, enemy):
        self.enemies.remove(enemy)
