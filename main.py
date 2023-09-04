import pygame
from game_logic import run_game
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders")
    run_game(screen)
    pygame.quit()