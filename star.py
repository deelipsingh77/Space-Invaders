import pygame
import random
from constants import SCREEN_WIDTH, COLORS

class Star:
    STAR_GENERATION_TIME = 0
    STAR_DELAY = 4000
    STAR_SPEED = 0.2

    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.size = random.randint(1, 3)
        self.y = -self.size
        self.speed = random.uniform(0.02, 0.04) if self.size <= 2 else Star.STAR_SPEED
        self.color = random.choice(COLORS)
    
    def move(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)