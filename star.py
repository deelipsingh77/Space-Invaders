import pygame
import random
from constants import SCREEN_WIDTH, COLORS

class Star:
    STAR_GENERATION_TIME = 0
    STAR_DELAY = 4000
    STAR_SPEED = 0.4

    def __init__(self):
        self.size = random.randint(1, 3)
        self.x = random.randint(0, SCREEN_WIDTH-self.size)
        self.y = -self.size
        self.speed = random.uniform(0.02,  Star.STAR_SPEED)
        self.color = random.choice(COLORS)
    
    def move(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)