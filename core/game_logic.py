import pygame
import graphics.assets as assets
import core.constants as constants
from core.constants import *
from entities.player import Player
from entities.star import Star
from entities.bullet import Bullet
from entities.enemy import Enemy
from entities.slime import Slime
from core.events import handle_keydown_event, handle_keyup_event
from graphics.menu import show_menu, show_settings
from core.highscore import reset_high_score

def run_game(screen):
    pygame.display.set_icon(assets.icon)
    clock = pygame.time.Clock()
    player = Player()

    enemies = []
    bullets = []
    slimes = []
    defeated = []
    stars = []

    Star.initial_stars(stars)

    running  = True
    while running:  
        screen.fill((0, 0, 0))
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if not constants.MENU_STATE:
                    handle_keydown_event(event.key, player, current_time, bullets, enemies, slimes)
                else:
                    if event.key == pygame.K_RETURN and not constants.settings:
                        if constants.option == 1:
                            constants.MENU_STATE = False
                        elif constants.option == 3:
                            running = False
                        else:
                            constants.settings = True
                    elif event.key == pygame.K_RETURN and constants.settings:
                        constants.settings = False
                        reset_high_score()
                            
                    if event.key == pygame.K_UP:
                        constants.option -= 1
                        if constants.option < 1:
                            constants.option = 3
                            
                    if event.key == pygame.K_DOWN:
                        constants.option += 1
                        if constants.option > 3:
                            constants.option = 1
                            
                    if event.key == pygame.K_ESCAPE:
                        constants.settings = False
                            
            if event.type == pygame.KEYUP:
                handle_keyup_event(event.key, player)

        Star.generate_stars(player, current_time, stars)
        Star.update_stars(screen, stars)
        
        if not constants.MENU_STATE:
            Bullet.create_bullet(player, current_time, bullets)
            Enemy.spawn_enemy(player, current_time, enemies) 

            args = [screen, player, current_time]
            Enemy.update_defeated(screen, current_time, defeated)
            Enemy.update_enemy(*args, enemies, slimes, defeated)
            Bullet.update_bullet(*args, bullets, enemies, slimes, defeated)
            Slime.update_slime(*args, slimes, defeated)
            Player.update_player(*args, enemies, bullets, slimes, defeated)
        else:
            if not constants.settings:
                show_menu(screen)
            else:
                show_settings(screen)

        pygame.display.update()
        clock.tick(FPS)