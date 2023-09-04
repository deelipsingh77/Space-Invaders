import pygame
import sys
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_HEIGHT, PLAYER_WIDTH
from assets import spaceship_img

class Player:
    def __init__(self):
        self.image = spaceship_img 
        self.x = (SCREEN_WIDTH - PLAYER_WIDTH) / 2
        self.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 30
        self.x_change = 0
        self.y_change = 0
        self.max_health = 100
        self.health = self.max_health
        self.explosion_time = sys.float_info.min
        self.defeat_time = sys.float_info.min
        self.crash_time = sys.float_info.min
        self.health_bar_time = sys.float_info.min
        self.width = PLAYER_WIDTH

    def move(self):
        self.x += self.x_change
        self.y += self.y_change
        self.x = max(0, min(SCREEN_WIDTH - PLAYER_WIDTH, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - PLAYER_HEIGHT, self.y))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
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
            pygame.draw.rect(screen, GRAY, (self.x, self.y + PLAYER_HEIGHT + 10, bar_width, bar_height))
            pygame.draw.rect(screen, COLOR, (self.x, self.y + PLAYER_HEIGHT + 10, health_width, bar_height))