import states
from assets import bullet_img

class Bullet:
    LAST_SHOT_TIME = 0
    FIRE_DELAY = 130
    BULLET_SPEED = 15
    SHOOT = False
    EXPLOSION_DELAY = 100

    def __init__(self, points):
        self.rect = bullet_img.get_rect(midtop = points)
        self.x , self.y = self.rect.center
        self.speed = Bullet.BULLET_SPEED
        self.damage = 10+((states.GAME_LEVEL-1)/10)

    def draw(self, screen):
        screen.blit(bullet_img, self.rect)

    def move(self):
        self.rect.top -= self.speed
    
    def fire(player):
        if player.health <= 0:
            player.health = 100
            player.PLAYER_SCORE = 0
        elif player.health > 0 and states.GAME_LEVEL < 6:
            Bullet.SHOOT = True

    def hold_fire():
        Bullet.SHOOT = False
