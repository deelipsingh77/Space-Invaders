import pygame
import states
from enemy import Enemy
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.font.init()

font = pygame.font.Font("assets/fonts/consola.ttf", 36)
font2 = pygame.font.Font("assets/fonts/consola.ttf", 25)
font3 = pygame.font.Font("assets/fonts/consolab.ttf", 150)

health_restored = font2.render("Health Restored! Max Health + 10", True, (255, 255, 255))
health_restored_rect = health_restored.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))

game_win_text = font.render("Press Enter to Play Again!", True, (255,255,255))
game_win_rect = game_win_text.get_rect(center = (SCREEN_WIDTH//2, (SCREEN_HEIGHT//2)+200))

game_over_text = font.render("Press Spacebar to Play Again!", True, (255,255,255))
game_over_rect = game_over_text.get_rect(center = (SCREEN_WIDTH//2, (SCREEN_HEIGHT//2)+200))

def level_display(screen):
    level_banner = font3.render(f"Level {states.GAME_LEVEL}", True, (255,255,255))
    level_banner_rect = level_banner.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(level_banner, level_banner_rect)
    if not Enemy.JUST_SPAWNED:
        screen.blit(health_restored, health_restored_rect)

def hud_display(screen):
    level_indicator =  font2.render(f"Level: {states.GAME_LEVEL}", True, (255,255,255))
    level_indicator_rect = level_indicator.get_rect(topleft = (10, 10))
    score_indicator = font2.render(f"Score: {states.PLAYER_SCORE}", True, (255,255,255))
    score_indicator_rect = score_indicator.get_rect(topright = (SCREEN_WIDTH-10, 10))
    screen.blit(level_indicator, level_indicator_rect)
    screen.blit(score_indicator, score_indicator_rect)
    states.draw_progress_bar(screen)