import attributes as atr
from constants import PLAYER_WIDTH
from assets import slime_img

class Slime:
    def __init__(self, enemy):
        self.rect = slime_img.get_rect(midbottom = enemy)
        self.speed = atr.SLIME_SPEED 
        self.damage = 10+((atr.GAME_LEVEL-1)/10)

    def move(self):
        self.rect.bottom += self.speed

    def draw(self, screen):
            screen.blit(slime_img, self.rect)