from melee_gun import MeleeGun
from global_functions import load_image
from images import sword, blue_sword


class Sword(MeleeGun):
    def __init__(self, scene, parent):
        super().__init__(scene, parent)

        image = sword
        self.set_image(image)
        self.rotate_speed = 400
        self.r = 0.75
        self.set_angles(-80, 80)
        self.damage = 25
        self.power = 5


class BlueSword(MeleeGun):
    def __init__(self, scene, parent):
        super().__init__(scene, parent)

        image = blue_sword
        self.set_image(image)
        self.rotate_speed = 200
        self.r = 0.75
        self.set_angles(-80, 80)
        self.damage = 25
        self.power = 1