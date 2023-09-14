import pygame
import assets
from game_logic import run_game
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from assets import *

if __name__ == "__main__":
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders")
    
    images = {    
        "icon_img": pygame.image.load(ICON_IMAGE_PATH).convert_alpha(),
        "enemy_img": [pygame.image.load(ENEMY_IMAGE).convert_alpha() for ENEMY_IMAGE in ENEMY_IMAGE_PATHS],
        "spaceship_img": pygame.image.load(SPACESHIP_IMAGE_PATH).convert_alpha(),
        "boss_img": [pygame.image.load(BOSS_IMAGE).convert_alpha() for BOSS_IMAGE in BOSS_IMAGE_PATHS],
        "bullet_img": pygame.image.load(BULLET_IMAGE_PATH).convert_alpha(),
        "slime_img": pygame.image.load(SLIME_IMAGE_PATH).convert_alpha(),
        "gameover_img": pygame.image.load(GAME_OVER_IMAGE_PATH).convert_alpha(),
        "youwin_img": pygame.image.load(YOU_WIN_IMAGE_PATH).convert_alpha(),
        "explode_img": pygame.image.load(EXPLODE_IMAGE_PATH).convert_alpha(),
        "explode2_img": pygame.image.load(EXPLODE_IMAGE_PATH2).convert_alpha(),
        "blast_img": pygame.image.load(BLASTING_IMAGE_PATH).convert_alpha(),
        "play_img": pygame.image.load(PLAY_IMAGE_PATH).convert_alpha(),
        "pause_img": pygame.image.load(PAUSE_IMAGE_PATH).convert_alpha()
    }
    
    assets.assign_assets(images)
    run_game(screen)
    pygame.quit()