from math import floor
from random import choice
from constants import WIDTH, HEIGHT, CAM_DX, CAM_DY, TILE_SIZE
from chunk import Chunk


class GameMap:
    def __init__(self, scene):
        self.scene = scene
        self.chunks = {}

        self.new_chunk((0, 0))

        self.to_delete = []
        self.to_add = []

    def get_start_player_pos(self):
        return self.chunks[choice(list(self.chunks.keys()))].get_start_player_pos()

    def get_at(self, coord):
        try:
            coord = floor(coord[0]), floor(coord[1])
            return self.chunks[(coord[0] // 20, coord[1] // 20)].tiles[coord[1] % 20][coord[0] % 20]
        except KeyError:
            return None

    def update(self, player):
        self.update_chunks(player)

    def update_chunks(self, player):
        cur_chunk = (player.coord[0] - (WIDTH / 2 + CAM_DX) / TILE_SIZE) // 20, \
                    (player.coord[1] - (HEIGHT / 2 + CAM_DY) / TILE_SIZE) // 20

        visible_chunks = []
        for d in [(0, 0), (1, 0), (0, 1), (1, 1)]:
            x = cur_chunk[0] + d[0]
            y = cur_chunk[1] + d[1]
            visible_chunks.append((x, y))
            if (x, y) not in self.chunks:
                if (x, y) not in self.to_add:
                    self.to_add.append((x, y))

        for number in self.chunks.keys():
            if number in visible_chunks:
                continue
            if number in self.to_add:
                continue
            if not self.chunks[number].is_on_the_cell():
                if number not in self.to_delete:
                    self.to_delete.append(number)

        if self.to_delete:
            self.delete_chunk(self.to_delete.pop())
        if self.to_add:
            self.new_chunk(self.to_add.pop())

    def new_chunk(self, number):
        self.chunks[number] = Chunk(self.scene, (number[0] * 20, number[1] * 20), self)

    def delete_chunk(self, number):
        self.chunks[number].delete()
        del self.chunks[number]
