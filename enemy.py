import pygame
import random
import sys
from constants import BOSS_SPEED, GAME_LEVEL, ENEMY_SPEED, SCREEN_WIDTH
from assets import load_image, ENEMY_IMAGE_PATHS, BOSS_IMAGE_PATHS

class Enemy:
    def __init__(self, isBoss):
        self.isBoss = isBoss
        if self.isBoss:
            self.height = 128
            self.width = 128
            self.x_change = BOSS_SPEED
            self.y_change = BOSS_SPEED
            self.max_health = 1000*GAME_LEVEL
            self.health = self.max_health
        else:
            self.x_change = ENEMY_SPEED
            self.y_change = ENEMY_SPEED
            self.height = 64
            self.width = 64
            self.max_health = 100+(GAME_LEVEL-1)*10
            self.health = self.max_health
        self.x = random.randint(0, SCREEN_WIDTH - 128)
        self.y = -self.height
        self.last_slime_time = 0
        self.spawn_time = 0
        self.h_move = False
        self.v_move = True
        self.start = -10
        self.enemy = random.choice([load_image(ENEMY_PATH) for ENEMY_PATH in ENEMY_IMAGE_PATHS])
        self.explosion_time = sys.float_info.min
        self.defeat_time = sys.float_info.min
        self.crash_time = sys.float_info.min
        self.health_bar_time = sys.float_info.min

    def spawn(self, screen):
        if not self.isBoss:
            screen.blit(self.enemy, (self.x, self.y))
        else:
            screen.blit(load_image(BOSS_IMAGE_PATHS[GAME_LEVEL-1]), (self.x, self.y))

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
                self.x_change = BOSS_SPEED
            else:
                self.x_change = ENEMY_SPEED
        elif self.x > SCREEN_WIDTH-self.width:
            self.x = SCREEN_WIDTH-self.width
            self.v_move = True
            self.h_move = False
            if self.isBoss:
                self.x_change = -BOSS_SPEED
            else:
                self.x_change = -ENEMY_SPEED
    
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