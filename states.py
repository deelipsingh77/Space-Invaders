import pygame
import states
from bullet import Bullet
from slime import Slime
from enemy import Enemy
from texts import game_over_text, game_over_rect, game_win_text, game_win_rect
from assets import gameover_img, play_img, pause_img, youwin_img
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_HEIGHT

# Timing
LEVEL_BANNER_TIME = 0
PLAY_TIME = 0

# Delays
LEVEL_DELAY = 3000
HEALTH_BAR_DELAY = 3000
PLAY_DELAY = 500

# Level
GAME_LEVEL = 1

# Game State
PAUSE_STATE = False

def reset(player, enemies, slimes, bullets):
    player.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT-PLAYER_HEIGHT)
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
    flush(enemies, slimes, bullets)

def flush(enemies, slimes, bullets):
    enemies.clear()
    slimes.clear()
    bullets.clear()

def gameover(screen, player, enemies, slimes, bullets):
    screen.blit(gameover_img, ((SCREEN_WIDTH-600)//2, (SCREEN_HEIGHT-309)//2))
    screen.blit(game_over_text,game_over_rect)
    states.reset(player, enemies, slimes, bullets)

def play(screen):
    screen.blit(play_img, ((SCREEN_WIDTH-128)//2, (SCREEN_HEIGHT-128)//2))

def pause(screen):
    screen.blit(pause_img, ((SCREEN_WIDTH-128)//2, (SCREEN_HEIGHT-128)//2))

def you_win(screen):
    screen.blit(youwin_img, ((SCREEN_WIDTH-256)//2, (SCREEN_HEIGHT-256)//2))
    screen.blit(game_win_text,game_win_rect)

def draw_progress_bar(screen):
    bar_height = 200
    bar_width = 5
    GRAY = (80, 80, 80)
    GREEN = (0, 180, 100)
    level_height = (Enemy.ENEMY_DESTROYED/(5*GAME_LEVEL)) * bar_height
    pygame.draw.rect(screen, GRAY, (0 , 200, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (0, 400-round(level_height), bar_width, level_height))