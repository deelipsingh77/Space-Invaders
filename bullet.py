import states
import assets
from enemy import Enemy
from slime import Slime

class Bullet:
    LAST_SHOT_TIME = 0
    FIRE_DELAY = 130
    BULLET_SPEED = 15
    SHOOT = False

    def __init__(self, points):
        self.rect = assets.images['bullet_img'].get_rect(midtop = points)
        self.x , self.y = self.rect.center
        self.speed = Bullet.BULLET_SPEED
        self.damage = 10+((states.GAME_LEVEL-1)/10)

    def draw(self, screen):
        screen.blit(assets.images['bullet_img'], self.rect)

    def move(self):
        self.rect.top -= self.speed
    
    def fire(player, *entities):
        if player.health <= 0:
            states.reset(player, *entities)
        elif player.health > 0 and states.GAME_LEVEL < 6:
            Bullet.SHOOT = True

    def hold_fire():
        Bullet.SHOOT = False

    @staticmethod
    def update_bullet(screen, player, current_time, bullets, enemies, slimes, defeated):
        for bullet in bullets:
            bullet.draw(screen)
            if not states.PAUSE_STATE:
                bullet.move()
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.health -= bullet.damage 
                    enemy.explosion_time = current_time
                    enemy.health_bar_time = current_time
                    try:
                        bullets.remove(bullet)
                    except ValueError:
                        pass
                    if enemy.health <= 0:
                        enemy.defeat_time = current_time
                        defeated.append(enemy)
                        states.PLAYER_SCORE += enemy.max_health
                        Enemy.ENEMY_DESTROYED += 1
                        if enemy.isBoss:
                            states.GAME_LEVEL += 1
                            Enemy.ENEMY_COUNT = 0
                            Enemy.ENEMY_DESTROYED = 0
                            Slime.SLIME_DELAY = 500 if Slime.SLIME_DELAY < 1000 else Slime.SLIME_DELAY - 500
                            Enemy.SPAWN_DELAY = 500 if Enemy.SPAWN_DELAY < 1000 else Enemy.SPAWN_DELAY - 500
                            Bullet.FIRE_DELAY -= (states.GAME_LEVEL-1)*10
                            player.health = 100 + (states.GAME_LEVEL - 1) * 10
                            player.max_health = 100 + (states.GAME_LEVEL - 1) * 10
                            Enemy.ENEMY_SPEED += 0.2
                            Enemy.BOSS_SPEED -= 0.1
                            Slime.SLIME_SPEED += 0.5
                            player.health_bar_time = current_time
                            states.LEVEL_BANNER_TIME = current_time
                            slimes.clear()
                        enemies.remove(enemy)

            if (bullet in bullets) and (bullet.rect.bottom < 0):
                bullets.remove(bullet) 

    @staticmethod
    def create_bullet(player, current_time, bullets):
        if current_time - Bullet.LAST_SHOT_TIME >= Bullet.FIRE_DELAY and not player.health <= 0 and Bullet.SHOOT and not states.WIN_STATE:
            new_bullet = Bullet(player.rect.midtop)
            bullets.append(new_bullet)
            Bullet.LAST_SHOT_TIME = current_time