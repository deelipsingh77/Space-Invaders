import pygame
import random
import attributes as atr
from constants import SCREEN_WIDTH, COLORS

class Star:
    def __init__(self):
        self.size = random.randint(1, 3)
        self.x = random.randint(0, SCREEN_WIDTH-self.size)
        self.y = -self.size
        self.speed = random.uniform(0.02, atr.STAR_SPEED)
        self.color = random.choice(COLORS)
    
    def move(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)