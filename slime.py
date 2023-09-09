import states
from constants import SCREEN_HEIGHT
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

    @staticmethod
    def update_slime(screen, player, current_time, slimes, defeated):
        for slime in slimes:
            slime.draw(screen)
            if not states.PAUSE_STATE:
                slime.move()

            if slime.rect.colliderect(player.rect):
                slimes.remove(slime)
                player.health -= slime.damage 
                player.explosion_time = current_time
                player.health_bar_time = current_time
                if player.health <= 0:
                    player.defeat_time = current_time
                    defeated.append(player)

            if (slime in slimes) and (slime.rect.top > SCREEN_HEIGHT):
                slimes.remove(slime)