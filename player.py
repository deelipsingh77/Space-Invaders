import pygame
import sys
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_HEIGHT, PLAYER_WIDTH
from assets import spaceship_img

class Player:
    CRASH_DELAY = 100
    PLAYER_SPEED = 5
    PLAYER_SCORE = 0

    def __init__(self):
        self.rect = spaceship_img.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT-PLAYER_HEIGHT))
        self.x, self.y = self.rect.center
        self.x_change = 0
        self.y_change = 0
        self.max_health = 100
        self.health = self.max_health
        self.explosion_time = sys.float_info.min
        self.defeat_time = sys.float_info.min
        self.crash_time = sys.float_info.min
        self.health_bar_time = sys.float_info.min

    def move(self):
        self.rect.centerx += self.x_change
        self.rect.centery += self.y_change
        self.rect.right = SCREEN_WIDTH if self.rect.right > SCREEN_WIDTH else self.rect.right
        self.rect.left = 0 if self.rect.left < 0 else self.rect.left
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = SCREEN_HEIGHT if self.rect.bottom > SCREEN_HEIGHT else self.rect.bottom

    def draw(self, screen):
        screen.blit(spaceship_img, self.rect)
    
    def draw_health_bar(self, screen):
        bar_width = PLAYER_WIDTH
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
            pygame.draw.rect(screen, GRAY, (self.rect.left, self.rect.bottom + 10, bar_width, bar_height))
            pygame.draw.rect(screen, COLOR, (self.rect.left, self.rect.bottom + 10, health_width, bar_height))