import pygame
import random
import math
import attributes as atr
from constants import *
from assets import icon_img, explode_img, blast_img, explode2_img
from player import Player
from star import Star
from bullet import Bullet
from enemy import Enemy
from slime import Slime
from states import gameover, play, pause, you_win
from texts import score_indicator, level_indicator, level_banner, health_restored, health_restored_rect

def run_game(screen):
    pygame.display.set_icon(icon_img)
    player = Player()

    enemies = []
    bullets = []
    slimes = []
    defeated = []
    stars = []

    # Initial Stars
    for i in range(random.randint(10, 15)):
        for j in range(random.randint(1, 5)):
            new_star = Star()
            new_star.y = random.randint(0, 600)
            stars.append(new_star)

    running  = True
    while running:
        #Background Color    
        screen.fill((0, 0, 0))

        current_time = pygame.time.get_ticks()



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.x_change = -1
                if event.key == pygame.K_RIGHT:
                    player.x_change = 1
                if event.key == pygame.K_UP:
                    player.y_change = -1
                if event.key == pygame.K_DOWN:
                    player.y_change = 1
                if event.key == pygame.K_RETURN:
                    if atr.GAME_LEVEL > 5:
                        atr.reset(player, enemies, slimes, bullets, defeated)

                if event.key == pygame.K_ESCAPE:
                    if atr.GAME_LEVEL < 6 and player.health > 0:
                        if atr.PAUSE_STATE:
                            atr.PLAY_TIME = current_time
                            atr.PAUSE_STATE = False
                        else:
                            atr.PAUSE_STATE = True
                if event.key == pygame.K_SPACE:
                    if player.health <= 0:
                        player.health = 100
                        atr.PLAYER_SCORE = 0
                    elif player.health > 0 and atr.GAME_LEVEL < 6:
                        atr.SHOOT = True

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    player.x_change = 0
                elif event.key in (pygame.K_UP, pygame.K_DOWN):
                    player.y_change = 0
                elif event.key == pygame.K_SPACE:
                    atr.SHOOT = False

        if current_time - atr.LAST_SHOT_TIME >= atr.FIRE_DELAY and not player.health <= 0 and atr.SHOOT:
            new_bullet = Bullet(player.x, player.y)
            bullets.append(new_bullet)
            atr.LAST_SHOT_TIME = current_time

        if (atr.JUST_SPAWNED or ((current_time - atr.LAST_SPAWN_TIME) >= atr.SPAWN_DELAY)) and not player.health <= 0 and not (current_time - atr.LEVEL_BANNER_TIME <= atr.LEVEL_DELAY) and not atr.PAUSE_STATE:
            if atr.ENEMY_COUNT < 5*atr.GAME_LEVEL:
                enemy_spawn = Enemy(False)
                enemies.append(enemy_spawn)
                atr.JUST_SPAWNED = False
                atr.LAST_SPAWN_TIME  = current_time
                enemy_spawn.spawn_time = current_time
                atr.ENEMY_COUNT += 1
            elif atr.ENEMY_COUNT == 5*atr.GAME_LEVEL:
                enemy_spawn = Enemy(True)
                enemies.append(enemy_spawn)
                atr.LAST_SPAWN_TIME  = current_time
                enemy_spawn.spawn_time = current_time
                atr.ENEMY_COUNT += 1
        
        if current_time - atr.STAR_GENERATION_TIME >= atr.STAR_DELAY and not player.health <= 0 and not atr.PAUSE_STATE:
            count = random.randint(3, 5)
            for i in range(count):
                new_star = Star()
                stars.append(new_star)
                atr.STAR_GENERATION_TIME = current_time
        
        for star in stars:
            star.draw(screen)
            if not atr.PAUSE_STATE:
                star.move()

            if star.y > SCREEN_HEIGHT:
                stars.remove(star)

        for enemy in enemies:
            enemy.spawn(screen)
            if not atr.PAUSE_STATE:
                enemy.move()

            if current_time - enemy.health_bar_time <= atr.HEALTH_BAR_DELAY:
                enemy.draw_health_bar(screen)
                
            if current_time - enemy.explosion_time <= atr.EXPLOSION_DELAY:
                screen.blit(explode_img, (enemy.x+(enemy.width)//2-12, enemy.y+(enemy.width)//2-12))

            if current_time - enemy.crash_time <= atr.EXPLOSION_DELAY:
                screen.blit(blast_img, (enemy.x+(enemy.width)//2-32, enemy.y+enemy.width-24))

            if (current_time - enemy.last_slime_time >= atr.SLIME_DELAY) and (current_time - enemy.spawn_time >= atr.SLIME_DELAY) and not atr.PAUSE_STATE:
                new_slime = Slime(enemy.x, enemy.y+48, enemy.width)
                slimes.append(new_slime)
                enemy.last_slime_time = current_time

            if math.sqrt(math.pow((enemy.x-player.x), 2)+math.pow((enemy.y-player.y), 2)) < 50 and not enemy.isBoss:
                enemy.crash_time = current_time
                player.crash_time = current_time
                player.health -= 10
                player.health_bar_time = current_time
            elif math.sqrt(math.pow((enemy.x+32-player.x), 2)+math.pow((enemy.y+32-player.y), 2)) < 100 and enemy.isBoss:
                enemy.crash_time = current_time
                player.crash_time = current_time
                player.health -= 10
                player.health_bar_time = current_time
            
            if enemy.y > SCREEN_HEIGHT:
                player.health = 0
                enemies.remove(enemy)
        
        for defeat in defeated:
            if current_time - defeat.defeat_time <= atr.EXPLOSION_DELAY:
                screen.blit(explode2_img, (defeat.x+(defeat.width)//2-32, defeat.y+(defeat.width)//2-32))
            else:
                defeated.remove(defeat)

        for bullet in bullets:
            bullet.draw(screen)
            if not atr.PAUSE_STATE:
                bullet.move()
            for enemy in enemies:
                if math.sqrt(math.pow((bullet.x+12-(enemy.x+(enemy.width/2)/2)), 2)+math.pow((bullet.y-(enemy.y+(enemy.width/2))), 2)) < enemy.width/2:
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
                        atr.PLAYER_SCORE += enemy.max_health
                        if enemy.isBoss:
                            atr.ENEMY_COUNT = 0
                            atr.GAME_LEVEL += 1
                            atr.SLIME_DELAY = 500 if atr.SLIME_DELAY < 1000 else atr.SLIME_DELAY - 500
                            atr.SPAWN_DELAY = 500 if atr.SPAWN_DELAY < 1000 else atr.SPAWN_DELAY - 500
                            atr.FIRE_DELAY -= (atr.GAME_LEVEL-1)*10
                            player.health = 100 + (atr.GAME_LEVEL - 1) * 10
                            player.max_health = 100 + (atr.GAME_LEVEL - 1) * 10
                            player.health_bar_time = current_time
                            atr.LEVEL_BANNER_TIME = current_time
                            atr.ENEMY_SPEED += 0.1
                            atr.BOSS_SPEED -= 0.05
                            slimes.clear()
                        enemies.remove(enemy)

            if (bullet in bullets) and (bullet.y < 0):
                bullets.remove(bullet) 

        for slime in slimes:
            slime.draw(screen)
            if not atr.PAUSE_STATE:
                slime.move()

            if (math.sqrt(math.pow((slime.x-player.x), 2)+math.pow((slime.y-player.y-24), 2))) < 37 and slime.enemy_width == PLAYER_WIDTH:
                slimes.remove(slime)
                player.health -= slime.damage 
                player.explosion_time = current_time
                player.health_bar_time = current_time
                if player.health == 0:
                    player.defeat_time = current_time
                    defeated.append(player)
            elif (math.sqrt(math.pow((slime.x-player.x+32), 2)+math.pow((slime.y-player.y-50), 2))) < 60 and slime.enemy_width == BOSS_WIDTH:
                slimes.remove(slime)
                player.health -= 10
                player.explosion_time = current_time
                player.health_bar_time = current_time
                if player.health == 0:
                    player.defeat_time = current_time
                    defeated.append(player)

            if slime.y > SCREEN_HEIGHT:
                slimes.remove(slime)

        if not player.health <= 0:
            if atr.GAME_LEVEL < 6:
                player.draw(screen)
                if not atr.PAUSE_STATE:
                    player.move()

                if current_time - atr.LEVEL_BANNER_TIME <= atr.LEVEL_DELAY:
                    levelBanner, levelBanner_rect = level_banner(atr.GAME_LEVEL)
                    screen.blit(levelBanner, levelBanner_rect)
                    if not atr.JUST_SPAWNED:
                        screen.blit(health_restored, health_restored_rect)

                if current_time - player.health_bar_time <= atr.HEALTH_BAR_DELAY:
                    player.draw_health_bar(screen)

                if current_time - player.explosion_time <= atr.EXPLOSION_DELAY:
                    screen.blit(explode_img, (player.x+(PLAYER_WIDTH)//2-12, player.y+(PLAYER_WIDTH)//2-12))

                if current_time - player.crash_time <= atr.CRASH_DELAY:
                    player.y += 10 

                if not (current_time - atr.LEVEL_BANNER_TIME <= atr.LEVEL_DELAY):
                    score, score_rect = score_indicator(atr.PLAYER_SCORE, "topright")
                    screen.blit(level_indicator(atr.GAME_LEVEL),(10, 10))
                    screen.blit(score, score_rect)

                if current_time - atr.PLAY_TIME <= atr.PLAY_DELAY and not (current_time - atr.LEVEL_BANNER_TIME <= atr.LEVEL_DELAY):
                    play(screen)

                if atr.PAUSE_STATE:
                    pause(screen)
            else:
                you_win(screen, player, enemies, slimes, bullets, defeated)
                score, score_rect = score_indicator(atr.PLAYER_SCORE, "center")
                screen.blit(score, score_rect)
        else:
            gameover(screen, player, enemies, slimes, bullets, defeated)
            score, score_rect = score_indicator(atr.PLAYER_SCORE, "center")
            screen.blit(score, score_rect)

        pygame.display.update()