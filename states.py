import pygame
import states
from bullet import Bullet
from slime import Slime
from enemy import Enemy
from texts import game_over_text, game_over_rect, game_win_text, game_win_rect, font2
from assets import gameover_img, play_img, pause_img, youwin_img
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_HEIGHT

# Timing
LEVEL_BANNER_TIME = 0
PLAY_TIME = 0

# Delays
LEVEL_DELAY = 3000
HEALTH_BAR_DELAY = 3000
PLAY_DELAY = 500
EXPLOSION_DELAY = 100

# Level
GAME_LEVEL = 1
PLAYER_SCORE = 0

# Game State
PAUSE_STATE = False
WIN_STATE = False

def reset(player, *entities):
    player.__init__()
    states.PLAYER_SCORE = 0
    states.GAME_LEVEL = 1
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
    states.WIN_STATE = False
    flush(*entities)

def flush(*entities):
    for entity in entities:
        entity.clear()

def gameover(screen, *entities):
    score_indicator = font2.render(f"Score: {states.PLAYER_SCORE}", True, (255,255,255))
    score_indicator_rect = score_indicator.get_rect(center = (SCREEN_WIDTH//2, (SCREEN_HEIGHT//2) + 250))

    if not states.WIN_STATE:
        screen.blit(gameover_img, ((SCREEN_WIDTH-600)//2, (SCREEN_HEIGHT-309)//2))
        screen.blit(game_over_text,game_over_rect)
    else:
        screen.blit(youwin_img, ((SCREEN_WIDTH-256)//2, (SCREEN_HEIGHT-256)//2))
        screen.blit(game_win_text,game_win_rect)

    screen.blit(score_indicator, score_indicator_rect)
    states.flush(*entities)

def play(screen):
    screen.blit(play_img, ((SCREEN_WIDTH-128)//2, (SCREEN_HEIGHT-128)//2))

def pause(screen):
    screen.blit(pause_img, ((SCREEN_WIDTH-128)//2, (SCREEN_HEIGHT-128)//2))

def toggle_pause(player, current_time):
    if GAME_LEVEL < 6 and player.health > 0:
        if states.PAUSE_STATE:
            states.PLAY_TIME = current_time
            states.PAUSE_STATE = False
        else:
            states.PAUSE_STATE = True

def draw_progress_bar(screen):
    bar_height = 200
    bar_width = 5
    GRAY = (80, 80, 80)
    GREEN = (0, 180, 100)
    level_height = (Enemy.ENEMY_DESTROYED/(5*GAME_LEVEL)) * bar_height
    pygame.draw.rect(screen, GRAY, (0 , 200, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (0, 400-round(level_height), bar_width, level_height))
