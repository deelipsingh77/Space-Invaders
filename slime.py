import states
from constants import PLAYER_WIDTH
from assets import slime_img

class Slime:
    SLIME_DELAY = 3000
    SLIME_SPEED = 5

    def __init__(self, enemy):
        self.rect = slime_img.get_rect(midbottom = enemy)
        self.x, self.y = self.rect.center
        self.speed = Slime.SLIME_SPEED 
        self.damage = 10+((states.GAME_LEVEL-1)/10)

    def move(self):
        self.rect.bottom += self.speed

    def draw(self, screen):
            screen.blit(slime_img, self.rect)