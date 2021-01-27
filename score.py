from text import Text
from constants import WIDTH, HEIGHT


class Score(Text):
    def __init__(self, size):
        super().__init__(size)
        self.coord = WIDTH // 2, HEIGHT / 8
        self.color = "white"
        self.set_score(0)

    def set_score(self, score):
        self.create(str(score), self.coord, self.color, center=True)
