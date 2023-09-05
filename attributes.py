from constants import SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_HEIGHT, PLAYER_WIDTH

# Timing
LAST_SHOT_TIME = 0
LAST_SPAWN_TIME = 0
LEVEL_BANNER_TIME = 0
PLAY_TIME = 0
STAR_GENERATION_TIME = 0

# Delays
FIRE_DELAY = 150
LEVEL_DELAY = 3000
SPAWN_DELAY = 5000
EXPLOSION_DELAY = 100
CRASH_DELAY = 100
HEALTH_BAR_DELAY = 3000
SLIME_DELAY = 3000
PLAY_DELAY = 500
STAR_DELAY = 4000

# Level and Progression
GAME_LEVEL = 1
ENEMY_COUNT = 0
ENEMY_SPEED = 0.3
BOSS_SPEED = 0.3
STAR_SPEED = 0.05

# Score and Points
PLAYER_SCORE = 0

# Game State
JUST_SPAWNED = True
PAUSE_STATE = False
SHOOT = False

def reset(player, enemies, slimes, bullets, defeated):
    global LAST_SHOT_TIME, LAST_SPAWN_TIME, ENEMY_COUNT, JUST_SPAWNED, FIRE_DELAY, SPAWN_DELAY, SLIME_DELAY, GAME_LEVEL, ENEMY_SPEED, BOSS_SPEED
    player.x = (SCREEN_WIDTH-PLAYER_WIDTH)/2
    player.y = (SCREEN_HEIGHT-PLAYER_HEIGHT)-30
    LAST_SHOT_TIME = 0
    LAST_SPAWN_TIME = 0
    ENEMY_COUNT = 0
    JUST_SPAWNED = True
    FIRE_DELAY = 150
    SPAWN_DELAY = 5000
    SLIME_DELAY = 3000
    GAME_LEVEL = 1
    ENEMY_SPEED = 0.3
    BOSS_SPEED = 0.3
    flush(enemies, slimes, bullets, defeated)

def flush(enemies, slimes, bullets, defeated):
    enemies.clear()
    slimes.clear()
    bullets.clear()
    defeated.clear()