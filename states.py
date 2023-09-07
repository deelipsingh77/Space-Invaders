import attributes as atr
import pygame
from texts import game_over_text, game_over_rect, game_win_text, game_win_rect
from assets import gameover_img, play_img, pause_img, youwin_img
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

def gameover(screen, player, enemies, slimes, bullets):
    gameover_img_rect = gameover_img.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(gameover_img, gameover_img_rect)
    screen.blit(game_over_text,game_over_rect)
    atr.reset(player, enemies, slimes, bullets)

def play(screen):
    screen.blit(play_img, ((SCREEN_WIDTH-128)//2, (SCREEN_HEIGHT-128)//2))

def pause(screen):
    screen.blit(pause_img, ((SCREEN_WIDTH-128)//2, (SCREEN_HEIGHT-128)//2))

def you_win(screen):
    screen.blit(youwin_img, ((SCREEN_WIDTH-256)//2, (SCREEN_HEIGHT-256)//2))
    screen.blit(game_win_text,game_win_rect)

def draw_health_bar(screen):
    bar_height = 200
    bar_width = 5
    GRAY = (80, 80, 80)
    GREEN = (0, 180, 100)
    level_height = (atr.MINION_COUNT/(5*atr.GAME_LEVEL)) * bar_height
    pygame.draw.rect(screen, GRAY, (0 , 200, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (0, 400-round(level_height), bar_width, level_height))
