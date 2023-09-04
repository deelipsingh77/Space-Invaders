from constants import GAME_LEVEL, PLAYER_WIDTH
from assets import load_image, SLIME_IMAGE_PATH

class Slime:
    def __init__(self, x, y, enemy_width):
        self.image = load_image(SLIME_IMAGE_PATH)
        self.x = x
        self.y = y
        self.speed = 1
        self.enemy_width = enemy_width
        self.damage = 10+((GAME_LEVEL-1)/10)

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        if self.enemy_width == PLAYER_WIDTH:
            screen.blit(self.image, (self.x + self.enemy_width/2 - 12, self.y - 12))
        else:
            screen.blit(self.image, (self.x + self.enemy_width/2 - 30, self.y - 12))
            screen.blit(self.image, (self.x + self.enemy_width/2 - 12, self.y - 12))
            screen.blit(self.image, (self.x + self.enemy_width/2 + 6, self.y - 12))