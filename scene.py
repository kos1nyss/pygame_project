from objects import ObjectWithSprite
from tiles import Tile
from shadows import Shadow
from player import Player
from gun import Gun
from ui_object import UiObject
from ability import Ability
from entity import Entity


class Scene:
    def __init__(self):
        self.objects = []
        self.with_sprites = []
        self.with_colliders = []

    def add(self, obj):
        self.objects.append(obj)
        if isinstance(obj, ObjectWithSprite) or isinstance(obj, Ability):
            self.with_sprites.append(obj)
            self.sort_objects_with_sprites()
        try:
            if obj.get_collider():
                self.with_colliders.append(obj)
        except AttributeError:
            pass

    def remove(self, cur_obj):
        if cur_obj in self.objects:
            self.objects.remove(cur_obj)

        if cur_obj in self.with_sprites:
            self.with_sprites.remove(cur_obj)

        if cur_obj in self.with_colliders:
            self.with_colliders.remove(cur_obj)

    def get_objects(self):
        return self.objects

    def get_objects_with_sprites(self):
        return self.with_sprites

    def sort_objects_with_sprites(self):
        self.with_sprites.sort(key=lambda obj: (isinstance(obj, Tile),
                                                isinstance(obj, Entity) and not isinstance(obj, Player),
                                                isinstance(obj, Shadow),
                                                isinstance(obj, Player),
                                                isinstance(obj, Gun),
                                                isinstance(obj, UiObject),
                                                isinstance(obj, Ability)),
                               reverse=True)

    def get_objects_with_colliders(self):
        return self.with_colliders
