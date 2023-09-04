import pygame

ICON_IMAGE_PATH = "assets/icon.png"
SPACESHIP_IMAGE_PATH = "assets/spaceship.png"
ENEMY_IMAGE_PATHS = ["assets/alien.png", "assets/ufo.png", "assets/monster2.png"] 
BOSS_IMAGE_PATHS = ["assets/monster.png", "assets/santelmo.png", "assets/alien2.png", "assets/kraken.png", "assets/cthulhu.png"]
BULLET_IMAGE_PATH = "assets/bullet.png"
SLIME_IMAGE_PATH = "assets/slime.png"
GAME_OVER_IMAGE_PATH = "assets/gameover.png"
YOU_WIN_IMAGE_PATH = "assets/you-win.png"
EXPLODE_IMAGE_PATH = "assets/explode.png"
EXPLODE_IMAGE_PATH2 = "assets/explode2.png"
BLASTING_IMAGE_PATH = "assets/blasting.png"
PLAY_IMAGE_PATH = "assets/play.png"
PAUSE_IMAGE_PATH = "assets/pause.png"

icon_img = pygame.image.load(ICON_IMAGE_PATH)
spaceship_img = pygame.image.load(SPACESHIP_IMAGE_PATH)
enemy_img = [pygame.image.load(ENEMY_IMAGE) for ENEMY_IMAGE in ENEMY_IMAGE_PATHS]
boss_img = [pygame.image.load(BOSS_IMAGE) for BOSS_IMAGE in BOSS_IMAGE_PATHS]
bullet_img = pygame.image.load(BULLET_IMAGE_PATH)
slime_img = pygame.image.load(SLIME_IMAGE_PATH)
gameover_img = pygame.image.load(GAME_OVER_IMAGE_PATH)
youwin_img = pygame.image.load(YOU_WIN_IMAGE_PATH)
explode_img = pygame.image.load(EXPLODE_IMAGE_PATH)
explode2_img = pygame.image.load(EXPLODE_IMAGE_PATH2)
blast_img = pygame.image.load(BLASTING_IMAGE_PATH)
play_img = pygame.image.load(PLAY_IMAGE_PATH)
pause_img = pygame.image.load(PAUSE_IMAGE_PATH)