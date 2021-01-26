import pygame


class LostGameScreen:
    def __init__(self):
        self.time = 0
        self.cd = 2

    def update(self, fps):
        self.time += 1 / fps
