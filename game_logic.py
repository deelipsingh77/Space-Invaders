import pygame
import random
import states 
from constants import *
from assets import icon_img, explode_img, blast_img, explode2_img
from player import Player
from star import Star
from bullet import Bullet
from enemy import Enemy
from slime import Slime
from states import gameover, play, pause, you_win
from texts import health_restored, health_restored_rect, font2, font3
from events import handle_keydown_event, handle_keyup_event

def run_game(screen):
    pygame.display.set_icon(icon_img)
    clock = pygame.time.Clock()
    player = Player()

    enemies = []
    bullets = []
    slimes = []
    defeated = []
    stars = []

    # Initial Stars
    for _ in range(random.randint(20, 30)):
        new_star = Star()
        new_star.y = random.randint(0, 600)
        stars.append(new_star)

    running  = True
    while running:
        #Background Color    
        screen.fill((0, 0, 0))

        current_time = pygame.time.get_ticks()

        level_indicator =  font2.render(f"Level: {states.GAME_LEVEL}", True, (255,255,255))
        level_indicator_rect = level_indicator.get_rect(topleft = (10, 10))
        score_indicator = font2.render(f"Score: {Player.PLAYER_SCORE}", True, (255,255,255))
        score_indicator_rect = score_indicator.get_rect(topright = (SCREEN_WIDTH-10, 10))
        level_banner = font3.render(f"Level {states.GAME_LEVEL}", True, (255,255,255))
        level_banner_rect = level_banner.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                handle_keydown_event(event.key, player, current_time, bullets, enemies, slimes)

            if event.type == pygame.KEYUP:
                handle_keyup_event(event.key, player)

        if current_time - Bullet.LAST_SHOT_TIME >= Bullet.FIRE_DELAY and not player.health <= 0 and Bullet.SHOOT:
            new_bullet = Bullet(player.rect.midtop)
            bullets.append(new_bullet)
            Bullet.LAST_SHOT_TIME = current_time

        if (Enemy.JUST_SPAWNED or (current_time - Enemy.LAST_SPAWN_TIME >= Enemy.SPAWN_DELAY)) and not (player.health <= 0 or current_time - states.LEVEL_BANNER_TIME <= states.LEVEL_DELAY or states.PAUSE_STATE or states.WIN_STATE):
            if Enemy.ENEMY_COUNT < 5*states.GAME_LEVEL:
                enemy_spawn = Enemy(False)
                enemies.append(enemy_spawn)
                Enemy.JUST_SPAWNED = False
                Enemy.LAST_SPAWN_TIME  = current_time
                enemy_spawn.spawn_time = current_time
                Enemy.ENEMY_COUNT += 1
            elif Enemy.ENEMY_COUNT == 5*states.GAME_LEVEL:
                enemy_spawn = Enemy(True)
                enemies.append(enemy_spawn)
                Enemy.LAST_SPAWN_TIME  = current_time
                enemy_spawn.spawn_time = current_time
                Enemy.ENEMY_COUNT += 1
        
        if current_time - Star.STAR_GENERATION_TIME >= Star.STAR_DELAY and not player.health <= 0 and not states.PAUSE_STATE:
            for i in range(random.randint(1, 4)):
                new_star = Star()
                stars.append(new_star)
                Star.STAR_GENERATION_TIME = current_time
        
        for star in stars:
            star.draw(screen)
            if not states.PAUSE_STATE:
                star.move()

            if star.y-star.size/2 > SCREEN_HEIGHT:
                stars.remove(star)

        for enemy in enemies:
            enemy.spawn(screen)
            if not states.PAUSE_STATE:
                enemy.move()

            if current_time - enemy.health_bar_time <= states.HEALTH_BAR_DELAY:
                enemy.draw_health_bar(screen)
                
            if current_time - enemy.explosion_time <= Bullet.EXPLOSION_DELAY:
                explode_img_rect = explode_img.get_rect(center = enemy.rect.center)
                screen.blit(explode_img, explode_img_rect)

            if current_time - enemy.crash_time <= Bullet.EXPLOSION_DELAY:
                blast_img_rect = blast_img.get_rect(midtop = enemy.rect.midbottom)
                screen.blit(blast_img, blast_img_rect)

            if (current_time - enemy.last_slime_time >= Slime.SLIME_DELAY) and (current_time - enemy.spawn_time >= Slime.SLIME_DELAY) and not states.PAUSE_STATE:
                if not enemy.isBoss:
                    slimes.append(Slime(enemy.rect.midbottom))
                else:
                    if states.GAME_LEVEL == 1:
                        new_slime = [Slime(enemy.rect.midbottom)]
                    elif states.GAME_LEVEL == 2:
                        new_slime = [Slime((enemy.rect.left + (enemy.rect.centerx-enemy.rect.left)//2, enemy.rect.bottom)), Slime((enemy.rect.centerx + (enemy.rect.right-enemy.rect.centerx)//2, enemy.rect.bottom))]
                    elif states.GAME_LEVEL >= 3:
                        new_slime = [Slime(enemy.rect.bottomleft), Slime(enemy.rect.midbottom), Slime(enemy.rect.bottomright)]
                    slimes.extend(new_slime)
                enemy.last_slime_time = current_time

            if player.rect.colliderect(enemy.rect):
                enemy.crash_time = current_time
                player.crash_time = current_time
                player.health -= 10
                player.health_bar_time = current_time
                if player.health <= 0:
                    player.defeat_time = current_time
                    defeated.append(player)
            
            if enemy.rect.bottom > SCREEN_HEIGHT:
                player.health = 0
                enemies.remove(enemy)
        
        for defeat in defeated:
            if current_time - defeat.defeat_time <= Bullet.EXPLOSION_DELAY:
                explode2_img_rect = explode2_img.get_rect(center = defeat.rect.center)
                screen.blit(explode2_img, explode2_img_rect)
            else:
                defeated.remove(defeat)

        for bullet in bullets:
            bullet.draw(screen)
            if not states.PAUSE_STATE:
                bullet.move()
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.health -= bullet.damage 
                    enemy.explosion_time = current_time
                    enemy.health_bar_time = current_time
                    try:
                        bullets.remove(bullet)
                    except ValueError:
                        pass
                    if enemy.health <= 0:
                        enemy.defeat_time = current_time
                        defeated.append(enemy)
                        Player.PLAYER_SCORE += enemy.max_health
                        Enemy.ENEMY_DESTROYED += 1
                        if enemy.isBoss:
                            states.GAME_LEVEL += 1
                            Enemy.ENEMY_COUNT = 0
                            Enemy.ENEMY_DESTROYED = 0
                            Slime.SLIME_DELAY = 500 if Slime.SLIME_DELAY < 1000 else Slime.SLIME_DELAY - 500
                            Enemy.SPAWN_DELAY = 500 if Enemy.SPAWN_DELAY < 1000 else Enemy.SPAWN_DELAY - 500
                            Bullet.FIRE_DELAY -= (states.GAME_LEVEL-1)*10
                            player.health = 100 + (states.GAME_LEVEL - 1) * 10
                            player.max_health = 100 + (states.GAME_LEVEL - 1) * 10
                            Enemy.ENEMY_SPEED += 0.2
                            Enemy.BOSS_SPEED -= 0.1
                            Slime.SLIME_SPEED += 0.5
                            player.health_bar_time = current_time
                            states.LEVEL_BANNER_TIME = current_time
                            slimes.clear()
                        enemies.remove(enemy)

            if (bullet in bullets) and (bullet.rect.bottom < 0):
                bullets.remove(bullet) 

        for slime in slimes:
            slime.draw(screen)
            if not states.PAUSE_STATE:
                slime.move()

            if slime.rect.colliderect(player.rect):
                slimes.remove(slime)
                player.health -= slime.damage 
                player.explosion_time = current_time
                player.health_bar_time = current_time
                if player.health <= 0:
                    player.defeat_time = current_time
                    defeated.append(player)

            if (slime in slimes) and (slime.rect.top > SCREEN_HEIGHT):
                slimes.remove(slime)

        if player.health > 0:
            if states.GAME_LEVEL < 6:
                player.draw(screen)
                if not states.PAUSE_STATE:
                    player.move()

                if current_time - states.LEVEL_BANNER_TIME <= states.LEVEL_DELAY:
                    screen.blit(level_banner, level_banner_rect)
                    if not Enemy.JUST_SPAWNED:
                        screen.blit(health_restored, health_restored_rect)

                if current_time - player.health_bar_time <= states.HEALTH_BAR_DELAY:
                    player.draw_health_bar(screen)

                if current_time - player.explosion_time <= Bullet.EXPLOSION_DELAY:
                    screen.blit(explode_img, player.rect)

                if current_time - player.crash_time <= Player.CRASH_DELAY:
                    player.rect.top += 20 

                if not (current_time - states.LEVEL_BANNER_TIME <= states.LEVEL_DELAY):
                    screen.blit(level_indicator, level_indicator_rect)
                    screen.blit(score_indicator, score_indicator_rect)
                    states.draw_progress_bar(screen)

                if current_time - states.PLAY_TIME <= states.PLAY_DELAY and not (current_time - states.LEVEL_BANNER_TIME <= states.LEVEL_DELAY):
                    play(screen)

                if states.PAUSE_STATE:
                    pause(screen)
            else:
                you_win(screen, enemies, slimes, bullets)
        else:
            gameover(screen, player, enemies, slimes, bullets)

        pygame.display.update()
        clock.tick(FPS)