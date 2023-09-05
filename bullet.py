import attributes as atr
from assets import bullet_img

class Bullet:
    def __init__(self, x, y):
        self.image = bullet_img 
        self.x = x
        self.y = y
        self.speed = 5
        self.damage = 10+((atr.GAME_LEVEL-1)/10)

    def draw(self, screen):
        screen.blit(self.image, (self.x + 32 - 12, self.y - 15))

    def move(self):
        self.y -= self.speed