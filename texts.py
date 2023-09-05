import pygame
import attributes as atr
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.font.init()

font = pygame.font.Font("assets/fonts/consolai.ttf", 36)
font2 = pygame.font.Font("assets/fonts/consola.ttf", 25)
font3 = pygame.font.Font("assets/fonts/consolab.ttf", 150)

health_restored = font2.render("Health Restored! Max Health + 10", True, (255, 255, 255))
health_restored_rect = health_restored.get_rect()
health_restored_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100)

game_win_text = font.render("Press Enter to Play Again!", True, (255,255,255))
game_win_rect = game_win_text.get_rect()
game_win_rect.center = (SCREEN_WIDTH//2, (SCREEN_HEIGHT//2)+200)

game_over_text = font.render("Press Spacebar to Play Again!", True, (255,255,255))
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (SCREEN_WIDTH//2, (SCREEN_HEIGHT//2)+200)