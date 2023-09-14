import pygame
import core.states as states
from entities.enemy import Enemy
from core.constants import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.font.init()

font = pygame.font.Font("assets/fonts/consola.ttf", 36)
font2 = pygame.font.Font("assets/fonts/consola.ttf", 25)
font3 = pygame.font.Font("assets/fonts/consolab.ttf", 150)
font4 = pygame.font.Font("assets/fonts/consola.ttf", 50)

health_restored = font2.render("Health Restored! Max Health + 10", True, (255, 255, 255))
health_restored_rect = health_restored.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))

game_win_text = font.render("Press Enter to Play Again!", True, (255,255,255))
game_win_rect = game_win_text.get_rect(center = (SCREEN_WIDTH//2, (SCREEN_HEIGHT//2)+200))

game_over_text = font.render("Press Spacebar to Play Again!", True, (255,255,255))
game_over_rect = game_over_text.get_rect(center = (SCREEN_WIDTH//2, (SCREEN_HEIGHT//2)+200))

def level_display(screen, current_time):
    if current_time - states.LEVEL_BANNER_TIME <= states.LEVEL_DELAY:
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
    
def play_text(color):
    play_game = font4.render("Play", True, color)
    play_game_rect = play_game.get_rect(midbottom = (SCREEN_WIDTH//2, (SCREEN_HEIGHT//2) + (SCREEN_HEIGHT//4)))
    return play_game, play_game_rect

def resume_text(color):
    resume_game = font4.render("Resume", True, color)
    resume_game_rect = resume_game.get_rect(midbottom = (SCREEN_WIDTH//2, (SCREEN_HEIGHT//2) + (SCREEN_HEIGHT//4)))
    return resume_game, resume_game_rect

def main_menu_text(color):
    return_game = font4.render("Main Menu", True, color)
    return_game_rect = return_game.get_rect(midbottom = (SCREEN_WIDTH//2, (SCREEN_HEIGHT//2) + (SCREEN_HEIGHT//4) + (SCREEN_HEIGHT//8)))
    return return_game, return_game_rect

def exit_text(color):
    exit_game = font4.render("Exit", True, color)
    exit_game_rect = exit_game.get_rect(midtop = (SCREEN_WIDTH//2, (SCREEN_HEIGHT//2) + (SCREEN_HEIGHT//4) + (SCREEN_HEIGHT//16)))
    return exit_game, exit_game_rect