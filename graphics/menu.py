import pygame
import core.constants as constants
from graphics.texts import play_game, play_game_rect, exit_game, exit_game_rect

def show_menu(screen):
    screen.fill((0, 0, 0))
    
    if constants.option:
        pygame.draw.rect(screen, (255, 0, 0), (play_game_rect.left, play_game_rect.top, play_game_rect.right-play_game_rect.left, play_game_rect.bottom-play_game_rect.top))
    else:
        pygame.draw.rect(screen, (255, 0, 0), (exit_game_rect.left, exit_game_rect.top, exit_game_rect.right-exit_game_rect.left, exit_game_rect.bottom-exit_game_rect.top))
        
    screen.blit(play_game, play_game_rect)
    screen.blit(exit_game, exit_game_rect)
    
    