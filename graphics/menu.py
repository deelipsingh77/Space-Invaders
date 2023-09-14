import pygame
import core.constants as constants
import graphics.assets as assets
from core.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from graphics.texts import play_game, play_game_rect, exit_game, exit_game_rect

def show_menu(screen):
    menu_img_resized = pygame.transform.scale(assets.images['menu_img'], (512, 221))
    menu_img_rect = menu_img_resized.get_rect(midbottom = (SCREEN_WIDTH//2, (SCREEN_HEIGHT//2)-40))
    screen.blit(menu_img_resized, menu_img_rect)
    
    if constants.option:
        vertices = [(play_game_rect.left - 20, play_game_rect.centery), (play_game_rect.left-50, play_game_rect.top), (play_game_rect.left-50, play_game_rect.bottom)]
        pygame.draw.polygon(screen, (255, 255, 255), vertices)
    else:
        vertices = [(exit_game_rect.left - 20, exit_game_rect.centery), (exit_game_rect.left-50, exit_game_rect.top), (exit_game_rect.left-50, exit_game_rect.bottom)]
        pygame.draw.polygon(screen, (255, 255, 255), vertices)
        
    screen.blit(play_game, play_game_rect)
    screen.blit(exit_game, exit_game_rect)