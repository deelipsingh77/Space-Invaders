import pygame
import random
import states
import sys
from constants import SCREEN_WIDTH, BOSS_HEIGHT, BOSS_WIDTH, PLAYER_HEIGHT, PLAYER_WIDTH
from assets import enemy_img, boss_img

class Enemy:
    JUST_SPAWNED = True
    SPAWN_DELAY = 5000
    LAST_SPAWN_TIME = sys.float_info.max
    ENEMY_COUNT = 0
    ENEMY_DESTROYED = 0
    ENEMY_SPEED = 1
    BOSS_SPEED = 0.8

    def __init__(self, isBoss):
        self.isBoss = isBoss
        if self.isBoss:
            self.enemy = boss_img[states.GAME_LEVEL-1] 
            self.height = BOSS_HEIGHT
            self.width = BOSS_WIDTH
            self.x_change = Enemy.BOSS_SPEED
            self.y_change = Enemy.BOSS_SPEED
            self.max_health = 1000*states.GAME_LEVEL
            self.health = self.max_health
            self.rect = self.enemy.get_rect(midbottom = (SCREEN_WIDTH//2, 0))
        else:
            self.enemy = random.choice(enemy_img)
            self.height = PLAYER_HEIGHT
            self.width = PLAYER_WIDTH
            self.x_change = Enemy.ENEMY_SPEED
            self.y_change = Enemy.ENEMY_SPEED
            self.max_health = 100+(states.GAME_LEVEL-1)*10
            self.health = self.max_health
            self.rect = self.enemy.get_rect(bottomright = (random.randint(self.width, SCREEN_WIDTH), 0))
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
            self.rect.bottom += self.y_change
            if self.rect.top - self.start > self.height+15:
                self.v_move = False
                self.h_move = True
                self.start = self.rect.top
        elif self.h_move:
            self.rect.centerx += self.x_change

        if self.rect.left < 0:
            self.rect.left = 0
            self.v_move = True
            self.h_move = False
            self.x_change = abs(self.x_change)
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.v_move = True
            self.h_move = False
            self.x_change = -self.x_change 
    
    def draw_health_bar(self, screen):
        bar_width = self.width
        bar_height = 5
        GRAY = (80, 80, 80)
        RED = (180, 0, 0)
        GREEN = (0, 180, 100)
        if (self.health / self.max_health)*100 < 25:
            COLOR = RED
        else:
            COLOR = GREEN
        
        health_width = (self.health / self.max_health) * bar_width
        if self.health != self.max_health:
            pygame.draw.rect(screen, GRAY, (self.rect.left , self.rect.top-10, bar_width, bar_height))
            pygame.draw.rect(screen, COLOR, (self.rect.left, self.rect.top-10, health_width, bar_height))