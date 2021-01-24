from constants import WIDTH, HEIGHT, TILE_SIZE, CAM_DX, CAM_DY
from objects import *
from tiles import Tile, EmptyTile
from shadows import Shadow
from shield import Shield
from melee_gun import MeleeGun
from ui_object import UiObject


class Camera(Object):
    def __init__(self, coord):
        super().__init__()
        self.set_coord(coord)
        self.target = None

    def apply(self, obj):
        if isinstance(obj, Tile):
            obj.rect.x = obj.get_coord()[0] * TILE_SIZE - self.coord[0] * TILE_SIZE
            obj.rect.y = obj.get_coord()[1] * TILE_SIZE - self.coord[1] * TILE_SIZE
        if isinstance(obj, ObjectWithMove) or isinstance(obj, Shadow):
            obj.rect.x = obj.get_coord()[0] * TILE_SIZE - self.coord[0] * TILE_SIZE
            obj.rect.y = obj.get_coord()[1] * TILE_SIZE - self.coord[
                1] * TILE_SIZE - obj.h * TILE_SIZE
        if isinstance(obj, Shield):
            obj.rect.x = obj.get_coord()[0] * TILE_SIZE - self.coord[
                0] * TILE_SIZE - obj.r + obj.parent.rect.w / 2
            obj.rect.y = obj.get_coord()[1] * TILE_SIZE - self.coord[
                1] * TILE_SIZE - obj.r - obj.parent.rect.h / 2
        if isinstance(obj, MeleeGun):
            obj.rect.x = obj.get_coord()[0] * TILE_SIZE - self.coord[0] * TILE_SIZE - obj.rect.w / 2 + obj.parent.rect.w / 2
            obj.rect.y = obj.get_coord()[1] * TILE_SIZE - self.coord[1] * TILE_SIZE - obj.rect.h / 2 - obj.parent.rect.h / 2
        if isinstance(obj, UiObject):
            obj.rect.x = obj.get_coord()[0] * TILE_SIZE - self.coord[0] * TILE_SIZE
            obj.rect.y = obj.get_coord()[1] * TILE_SIZE - self.coord[1] * TILE_SIZE
        if isinstance(obj, ObjectWithSprite) or isinstance(obj, Shield):
            obj.rect.x += WIDTH / 2 - TILE_SIZE / 2 + CAM_DX
            obj.rect.y += HEIGHT / 2 - TILE_SIZE / 2 + CAM_DY

    def look_at(self, obj):
        self.set_coord(obj.get_coord())

    def set_target(self, target):
        self.target = target

    def get_target(self):
        return self.target

    def follow_up(self):
        self.move((self.target.dx, self.target.dy))
