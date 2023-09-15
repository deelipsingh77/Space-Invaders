import random
import sys
import core.states as states
import graphics.assets as assets
from core.constants import SCREEN_WIDTH, BOSS_HEIGHT, BOSS_WIDTH, PLAYER_HEIGHT, PLAYER_WIDTH, SCREEN_HEIGHT
from graphics.damage import damage_display, explosion_display
from entities.slime import Slime
from graphics.healthbar import health_bar_display

class Enemy:
    JUST_SPAWNED = True
    SPAWN_DELAY = 5000
    LAST_SPAWN_TIME = sys.float_info.max
    ENEMY_COUNT = 0
    ENEMY_DESTROYED = 0
    ENEMY_SPEED = 1
    BOSS_SPEED = 0.8
    V_MOVE_COUNT = 0

    def __init__(self, isBoss):
        self.isPlayer = False
        self.isBoss = isBoss
        if self.isBoss:
            self.enemy = assets.images['boss_img'][states.GAME_LEVEL-1] 
            self.height = BOSS_HEIGHT
            self.width = BOSS_WIDTH
            self.x_change = Enemy.BOSS_SPEED
            self.y_change = Enemy.BOSS_SPEED
            self.max_health = 1000*states.GAME_LEVEL
            self.health = self.max_health
        else:
            self.enemy = random.choice(assets.images['enemy_img'])
            self.height = PLAYER_HEIGHT
            self.width = PLAYER_WIDTH
            self.x_change = Enemy.ENEMY_SPEED
            self.y_change = Enemy.ENEMY_SPEED
            self.max_health = 100+(states.GAME_LEVEL-1)*10
            self.health = self.max_health
        self.rect = self.enemy.get_rect(midbottom = (random.randint(0, SCREEN_WIDTH - self.width/2), 0))
        self.start = self.rect.top
        self.h_move = False
        self.v_move = True
        self.last_slime_time = 0
        self.spawn_time = 0
        self.explosion_time = sys.float_info.min
        self.defeat_time = sys.float_info.min
        self.crash_time = sys.float_info.min
        self.health_bar_time = sys.float_info.min

    def spawn(self, screen):
            screen.blit(self.enemy, self.rect)

    def move(self):
        if self.v_move:
            if not self.isBoss:
                self.rect.bottom += self.y_change
            else:
                if Enemy.V_MOVE_COUNT < 3 or Enemy.V_MOVE_COUNT >= 5:
                    self.rect.bottom += self.y_change
                elif Enemy.V_MOVE_COUNT in (3, 4):
                    self.rect.bottom -= self.y_change
                    
            if abs(self.rect.top - self.start) > self.height+15:
                self.v_move = False
                self.h_move = True
                self.start = self.rect.top
        elif self.h_move:
            self.rect.centerx += self.x_change

        if self.rect.left < 0:
            if self.isBoss:
                Enemy.V_MOVE_COUNT += 1
            self.rect.left = 0
            self.v_move = True
            self.h_move = False
            self.x_change = abs(self.x_change)
        elif self.rect.right > SCREEN_WIDTH:
            if self.isBoss:
                Enemy.V_MOVE_COUNT += 1
            self.rect.right = SCREEN_WIDTH
            self.v_move = True
            self.h_move = False
            self.x_change = -self.x_change 
    
    @staticmethod
    def update_enemy(screen, player, current_time, enemies, slimes, defeated):
        for enemy in enemies:
            enemy.spawn(screen)
            if not states.PAUSE_STATE:
                enemy.move()

            health_bar_display(screen, enemy, current_time)
            damage_display(screen, enemy, current_time)
            explosion_display(screen, enemy, current_time) 

            Slime.create_slime(enemy, current_time, slimes)

            if player.rect.colliderect(enemy.rect):
                enemy.crash_time = current_time
                player.crash_time = current_time
                player.health -= 10
                player.health_bar_time = current_time
                if player.health <= 0:
                    player.defeat_time = current_time
                    defeated.append(player)
            
            if enemy.rect.bottom > SCREEN_HEIGHT:
                player.health = 0
                enemies.remove(enemy)

    @staticmethod
    def spawn_enemy(player, current_time, enemies):
        if (Enemy.JUST_SPAWNED or (current_time - Enemy.LAST_SPAWN_TIME >= Enemy.SPAWN_DELAY)) and not (player.health <= 0 or current_time - states.LEVEL_BANNER_TIME <= states.LEVEL_DELAY or states.PAUSE_STATE or states.WIN_STATE):
            if Enemy.ENEMY_COUNT < 5*states.GAME_LEVEL:
                enemy_spawn = Enemy(False)
                enemies.append(enemy_spawn)
                Enemy.JUST_SPAWNED = False
                Enemy.LAST_SPAWN_TIME  = current_time
                enemy_spawn.spawn_time = current_time
                Enemy.ENEMY_COUNT += 1
            elif Enemy.ENEMY_COUNT == 5*states.GAME_LEVEL:
                enemy_spawn = Enemy(True)
                enemies.append(enemy_spawn)
                Enemy.LAST_SPAWN_TIME  = current_time
                enemy_spawn.spawn_time = current_time
                Enemy.ENEMY_COUNT += 1

    @staticmethod
    def update_defeated(screen, current_time, defeated):
        for defeat in defeated:
            if current_time - defeat.defeat_time <= states.EXPLOSION_DELAY:
                explode2_img_rect = assets.images['explode2_img'].get_rect(center = defeat.rect.center)
                screen.blit(assets.images['explode2_img'], explode2_img_rect)
            else:
                defeated.remove(defeat)