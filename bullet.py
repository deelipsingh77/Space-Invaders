import attributes as atr
from assets import bullet_img

class Bullet:
    def __init__(self, points):
        self.rect = bullet_img.get_rect(midtop = points)
        self.speed = atr.BULLET_SPEED
        self.damage = 10+((atr.GAME_LEVEL-1)/10)

    def draw(self, screen):
        screen.blit(bullet_img, self.rect)

    def move(self):
        self.rect.top -= self.speed