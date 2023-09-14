import states
import assets
from constants import SCREEN_HEIGHT

class Slime:
    SLIME_DELAY = 3000
    SLIME_SPEED = 5

    def __init__(self, enemy):
        self.rect = assets.images['slime_img'].get_rect(midbottom = enemy)
        self.x, self.y = self.rect.center
        self.speed = Slime.SLIME_SPEED 
        self.damage = 10+((states.GAME_LEVEL-1)/10)

    def move(self):
        self.rect.bottom += self.speed

    def draw(self, screen):
            screen.blit(assets.images['slime_img'], self.rect)

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

    @staticmethod
    def create_slime(enemy, current_time, slimes):
        if (current_time - enemy.last_slime_time >= Slime.SLIME_DELAY) and (current_time - enemy.spawn_time >= Slime.SLIME_DELAY) and not states.PAUSE_STATE:
            if not enemy.isBoss:
                slimes.append(Slime(enemy.rect.midbottom))
            else:
                if states.GAME_LEVEL == 1:
                    new_slime = [Slime(enemy.rect.midbottom)]
                elif states.GAME_LEVEL == 2:
                    new_slime = [Slime((enemy.rect.left + (enemy.rect.centerx-enemy.rect.left)//2, enemy.rect.bottom)), Slime((enemy.rect.centerx + (enemy.rect.right-enemy.rect.centerx)//2, enemy.rect.bottom))]
                elif states.GAME_LEVEL >= 3:
                    new_slime = [Slime(enemy.rect.bottomleft), Slime(enemy.rect.midbottom), Slime(enemy.rect.bottomright)]
                slimes.extend(new_slime)
            enemy.last_slime_time = current_time
