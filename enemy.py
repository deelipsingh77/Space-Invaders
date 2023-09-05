import pygame
import random
import sys
import attributes as atr
from constants import SCREEN_WIDTH, BOSS_HEIGHT, BOSS_WIDTH, PLAYER_HEIGHT, PLAYER_WIDTH
from assets import enemy_img, boss_img

class Enemy:
    def __init__(self, isBoss):
        self.isBoss = isBoss
        if self.isBoss:
            self.enemy = boss_img[atr.GAME_LEVEL-1] 
            self.height = BOSS_HEIGHT
            self.width = BOSS_WIDTH
            self.x_change = atr.BOSS_SPEED
            self.y_change = atr.BOSS_SPEED
            self.max_health = 1000*atr.GAME_LEVEL
            self.health = self.max_health
        else:
            self.enemy = random.choice(enemy_img)
            self.x_change = atr.ENEMY_SPEED
            self.y_change = atr.ENEMY_SPEED
            self.height = PLAYER_HEIGHT
            self.width = PLAYER_WIDTH
            self.max_health = 100+(atr.GAME_LEVEL-1)*10
            self.health = self.max_health
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = -self.height
        self.last_slime_time = 0
        self.spawn_time = 0
        self.h_move = False
        self.v_move = True
        self.start = -10
        self.explosion_time = sys.float_info.min
        self.defeat_time = sys.float_info.min
        self.crash_time = sys.float_info.min
        self.health_bar_time = sys.float_info.min

    def spawn(self, screen):
            screen.blit(self.enemy, (self.x, self.y))

    def move(self):
        if self.v_move:
            self.y += self.y_change
            if round(self.y - self.start) > 70:
                self.v_move = False
                self.h_move = True
                self.start = self.y
        elif self.h_move:
            self.x += self.x_change

        if self.x < 0:
            self.x = 0
            self.v_move = True
            self.h_move = False
            if self.isBoss:
                self.x_change = atr.BOSS_SPEED
            else:
                self.x_change = atr.ENEMY_SPEED
        elif self.x > SCREEN_WIDTH-self.width:
            self.x = SCREEN_WIDTH-self.width
            self.v_move = True
            self.h_move = False
            if self.isBoss:
                self.x_change = -atr.BOSS_SPEED
            else:
                self.x_change = -atr.ENEMY_SPEED
    
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
            pygame.draw.rect(screen, GRAY, (self.x, self.y-10, bar_width, bar_height))
            pygame.draw.rect(screen, COLOR, (self.x, self.y-10, health_width, bar_height))