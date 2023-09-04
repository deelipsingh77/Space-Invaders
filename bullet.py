from assets import load_image, BULLET_IMAGE_PATH
from constants import GAME_LEVEL

class Bullet:
    def __init__(self, x, y):
        self.image = load_image(BULLET_IMAGE_PATH)
        self.x = x
        self.y = y
        self.speed = 5
        self.damage = 10+((GAME_LEVEL-1)/10)

    def draw(self, screen):
        screen.blit(self.image, (self.x + 32 - 12, self.y - 15))

    def move(self):
        self.y -= self.speed