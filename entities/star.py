import pygame
import random
import core.states as states
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS

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
    
    @staticmethod
    def initial_stars(stars):
        for _ in range(random.randint(20, 30)):
            new_star = Star()
            new_star.y = random.randint(0, 600)
            stars.append(new_star)

    @staticmethod
    def update_stars(screen, stars):
        for star in stars:
            star.draw(screen)
            if not states.PAUSE_STATE:
                star.move()

            if star.y > SCREEN_HEIGHT:
                stars.remove(star)

    @staticmethod
    def generate_stars(player, current_time, stars):
        if current_time - Star.STAR_GENERATION_TIME >= Star.STAR_DELAY and not player.health <= 0 and not states.PAUSE_STATE:
            for _ in range(random.randint(1, 4)):
                new_star = Star()
                stars.append(new_star)
                Star.STAR_GENERATION_TIME = current_time