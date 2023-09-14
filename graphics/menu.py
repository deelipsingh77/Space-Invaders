import pygame
import core.constants as constants
import graphics.assets as assets
from core.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from core.highscore import get_high_score
from graphics.texts import font2, font4, play_text, exit_text

def show_menu(screen):
    play = None
    exit = None
    if get_high_score() != 0:
        high_score = font2.render(f"High Score: {get_high_score()}", True, (255, 255, 255))
        high_score_rect = high_score.get_rect(bottomright = (SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10))
        screen.blit(high_score, high_score_rect)
        
    tomato = (255, 99, 71)
    white = (255, 255, 255)    
    
    menu_img_resized = pygame.transform.scale(assets.images['menu_img'], (512, 221))
    menu_img_rect = menu_img_resized.get_rect(midbottom = (SCREEN_WIDTH//2, (SCREEN_HEIGHT//2)-40))
    screen.blit(menu_img_resized, menu_img_rect)
    
    if constants.option:
        play = play_text(tomato)
        exit = exit_text(white)
        
        vertices = [(play[1].left - 20, play[1].centery), (play[1].left-50, play[1].top), (play[1].left-50, play[1].bottom)]
        pygame.draw.polygon(screen, tomato, vertices)
    else:
        play = play_text(white)
        exit = exit_text(tomato)
        vertices = [(exit[1].left - 20, exit[1].centery), (exit[1].left-50, exit[1].top), (exit[1].left-50, exit[1].bottom)]
        pygame.draw.polygon(screen, tomato, vertices)
        
    screen.blit(*play)
    screen.blit(*exit)