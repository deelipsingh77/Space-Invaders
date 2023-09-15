import pygame
import graphics.assets as assets
import core.constants as constants
from entities.bullet import Bullet
from entities.slime import Slime
from entities.enemy import Enemy
from graphics.texts import game_over_text, game_over_rect, game_win_text, game_win_rect, font2
from core.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from graphics.menu import pause_menu

# Timing
LEVEL_BANNER_TIME = 0
PLAY_TIME = 0

# Delays
LEVEL_DELAY = 3000
HEALTH_BAR_DELAY = 3000
PLAY_DELAY = 500
EXPLOSION_DELAY = 100
V_MOVE_COUNT = 0

# Level
GAME_LEVEL = 1
PLAYER_SCORE = 0

# Game State
PAUSE_STATE = False
WIN_STATE = False
GAME_OVER = False

def reset(player, *entities):
    global PLAYER_SCORE, GAME_LEVEL, WIN_STATE, PAUSE_STATE, V_MOVE_COUNT
    player.__init__()
    GAME_LEVEL = 1
    Bullet.LAST_SHOT_TIME = 0
    Bullet.FIRE_DELAY = 150
    Slime.SLIME_DELAY = 3000
    Enemy.JUST_SPAWNED = True
    Enemy.ENEMY_COUNT = 0
    Enemy.SPAWN_DELAY = 5000
    Enemy.LAST_SPAWN_TIME = 0
    Enemy.ENEMY_SPEED = 1
    Enemy.BOSS_SPEED = 1
    Enemy.ENEMY_DESTROYED = 0
    WIN_STATE = False
    PAUSE_STATE = False
    constants.option = 1
    constants.pause_option = True
    constants.settings = False
    V_MOVE_COUNT = 0
    flush(*entities)

def flush(*entities):
    for entity in entities:
        entity.clear()

def gameover(screen, player, *entities):
    score_indicator = font2.render(f"Score: {PLAYER_SCORE}", True, (255,255,255))
    score_indicator_rect = score_indicator.get_rect(center = (SCREEN_WIDTH//2, (SCREEN_HEIGHT//2) + 250))

    if not WIN_STATE:
        screen.blit(assets.images['gameover_img'], ((SCREEN_WIDTH-600)//2, (SCREEN_HEIGHT-309)//2))
        screen.blit(game_over_text,game_over_rect)
    else:
        screen.blit(assets.images['youwin_img'], ((SCREEN_WIDTH-256)//2, (SCREEN_HEIGHT-256)//2))
        screen.blit(game_win_text,game_win_rect)

    screen.blit(score_indicator, score_indicator_rect)
    reset(player, *entities)

def play(screen):
    screen.blit(assets.images['play_img'], ((SCREEN_WIDTH-128)//2, (SCREEN_HEIGHT-128)//2))

def pause(screen):
    pause_menu(screen)
    screen.blit(assets.images['pause_img'], ((SCREEN_WIDTH-128)//2, (SCREEN_HEIGHT-128)//2))

def toggle_pause(player, current_time):
    global PLAY_TIME, PAUSE_STATE
    if GAME_LEVEL < 6 and player.health > 0:
        if PAUSE_STATE:
            PLAY_TIME = current_time
            PAUSE_STATE = False
        else:
            PAUSE_STATE = True

def draw_progress_bar(screen):
    bar_height = 200
    bar_width = 5
    GRAY = (80, 80, 80)
    GREEN = (0, 180, 100)
    level_height = (Enemy.ENEMY_DESTROYED/(5*GAME_LEVEL)) * bar_height
    pygame.draw.rect(screen, GRAY, (0 , 200, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (0, 400-round(level_height), bar_width, level_height))