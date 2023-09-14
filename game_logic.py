import pygame
import assets
from constants import *
from player import Player
from star import Star
from bullet import Bullet
from enemy import Enemy
from slime import Slime
from events import handle_keydown_event, handle_keyup_event

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
                handle_keydown_event(event.key, player, current_time, bullets, enemies, slimes)

            if event.type == pygame.KEYUP:
                handle_keyup_event(event.key, player)

        Bullet.create_bullet(player, current_time, bullets)
        Enemy.spawn_enemy(player, current_time, enemies) 
        Star.generate_stars(player, current_time, stars)

        args = [screen, player, current_time]
        Star.update_stars(screen, stars)
        Enemy.update_defeated(screen, current_time, defeated)
        Enemy.update_enemy(*args, enemies, slimes, defeated)
        Bullet.update_bullet(*args, bullets, enemies, slimes, defeated)
        Slime.update_slime(*args, slimes, defeated)
        Player.update_player(*args, enemies, bullets, slimes, defeated)

        pygame.display.update()
        clock.tick(FPS)