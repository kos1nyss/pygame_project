from melee_gun import MeleeGun
from global_functions import load_image


class Sword(MeleeGun):
    def __init__(self, scene, parent):
        super().__init__(scene, parent)

        image = load_image("sword.png")
        self.set_image(image)
        self.rotate_speed = 400
        self.r = 0.75
        self.set_angles(-80, 80)
        self.damage = 25
