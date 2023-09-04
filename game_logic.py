import pygame
import random
import math
from constants import *
from assets import icon_img, explode_img, blast_img, explode2_img, pause_img, gameover_img, play_img, youwin_img
from player import Player
from star import Star
from bullet import Bullet
from enemy import Enemy
from slime import Slime

def run_game(screen):
    global LAST_SHOT_TIME, LAST_SPAWN_TIME, LEVEL_BANNER_TIME, PLAY_TIME, JUST_SPAWNED, FIRE_DELAY, LEVEL_DELAY, SPAWN_DELAY, EXPLOSION_DELAY, CRASH_DELAY, HEALTH_BAR_DELAY, SLIME_DELAY, PLAY_DELAY, STAR_DELAY, ENEMY_COUNT, GAME_LEVEL, ENEMY_SPEED, BOSS_SPEED, STAR_SPEED, PLAYER_SCORE, STAR_GENERATION_TIME, COLORS, PAUSE_STATE, SHOOT

    pygame.display.set_icon(icon_img)

    font = pygame.font.Font("assets/fonts/consolai.ttf", 36)
    font2 = pygame.font.Font("assets/fonts/consola.ttf", 25)
    font3 = pygame.font.Font("assets/fonts/consolab.ttf", 150)

    health_restored = font2.render("Health Restored! Max Health + 10", True, (255, 255, 255))
    health_restored_rect = health_restored.get_rect()
    health_restored_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100)

    game_win_text = font.render("Press Enter to Play Again!", True, (255,255,255))
    game_win_rect = game_win_text.get_rect()
    game_win_rect.center = (SCREEN_WIDTH//2, (SCREEN_HEIGHT//2)+200)

    game_over_text = font.render("Press Spacebar to Play Again!", True, (255,255,255))
    game_over_rect = game_over_text.get_rect()
    game_over_rect.center = (SCREEN_WIDTH//2, (SCREEN_HEIGHT//2)+200)

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

    def gameover():
        screen.blit(gameover_img, ((SCREEN_WIDTH-600)//2, (SCREEN_HEIGHT-309)//2))
        screen.blit(game_over_text,game_over_rect)
        reset()

    def play():
        screen.blit(play_img, ((SCREEN_WIDTH-128)//2, (SCREEN_HEIGHT-128)//2))

    def pause():
        screen.blit(pause_img, ((SCREEN_WIDTH-128)//2, (SCREEN_HEIGHT-128)//2))

    def you_win():
        global PAUSE_STATE
        screen.blit(youwin_img, ((SCREEN_WIDTH-256)//2, (SCREEN_HEIGHT-256)//2))
        screen.blit(game_win_text,game_win_rect)
        PAUSE_STATE = True

    def reset():
        global SPAWN_DELAY, FIRE_DELAY, LAST_SHOT_TIME, LAST_SPAWN_TIME, ENEMY_COUNT, JUST_SPAWNED, SLIME_DELAY, GAME_LEVEL, ENEMY_SPEED, BOSS_SPEED
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
        enemies.clear()
        slimes.clear()
        bullets.clear()
        defeated.clear()

    running  = True
    while running:
        #Background Color    
        screen.fill((0, 0, 0))

        current_time = pygame.time.get_ticks()

        level_indicator = font2.render(f"Level: {GAME_LEVEL}", True, (255,255,255))
        score_indicator = font2.render(f"Score: {PLAYER_SCORE}", True, (255,255,255))
        level_banner = font3.render(f"Level {GAME_LEVEL}", True, (255,255,255))

        score_indicator_rect = score_indicator.get_rect()
        level_banner_rect = level_banner.get_rect()

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
                    if GAME_LEVEL > 5:
                        reset()

                if event.key == pygame.K_ESCAPE:
                    if GAME_LEVEL < 6 and player.health > 0:
                        if PAUSE_STATE:
                            PLAY_TIME = current_time
                            PAUSE_STATE = False
                        else:
                            PAUSE_STATE = True
                if event.key == pygame.K_SPACE:
                    if player.health <= 0:
                        player.health = 100
                        PLAYER_SCORE = 0
                    elif player.health > 0 and GAME_LEVEL < 6:
                        SHOOT = True

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    player.x_change = 0
                elif event.key in (pygame.K_UP, pygame.K_DOWN):
                    player.y_change = 0
                elif event.key == pygame.K_SPACE:
                    SHOOT = False

        if current_time - LAST_SHOT_TIME >= FIRE_DELAY and not player.health <= 0 and SHOOT:
            new_bullet = Bullet(player.x, player.y)
            bullets.append(new_bullet)
            LAST_SHOT_TIME = current_time

        if (JUST_SPAWNED or ((current_time - LAST_SPAWN_TIME) >= SPAWN_DELAY)) and not player.health <= 0 and not (current_time - LEVEL_BANNER_TIME <= LEVEL_DELAY) and not PAUSE_STATE:
            if ENEMY_COUNT < 5*GAME_LEVEL:
                enemy_spawn = Enemy(False)
                enemies.append(enemy_spawn)
                JUST_SPAWNED = False
                LAST_SPAWN_TIME  = current_time
                enemy_spawn.spawn_time = current_time
                ENEMY_COUNT += 1
            elif ENEMY_COUNT == 5*GAME_LEVEL:
                enemy_spawn = Enemy(True)
                enemies.append(enemy_spawn)
                LAST_SPAWN_TIME  = current_time
                enemy_spawn.spawn_time = current_time
                ENEMY_COUNT += 1
        
        if current_time - STAR_GENERATION_TIME >= STAR_DELAY and not player.health <= 0 and not PAUSE_STATE:
            count = random.randint(3, 5)
            for i in range(count):
                new_star = Star()
                stars.append(new_star)
                STAR_GENERATION_TIME = current_time
        
        for star in stars:
            star.draw(screen)
            if not PAUSE_STATE:
                star.move()

            if star.y > SCREEN_HEIGHT:
                stars.remove(star)

        for enemy in enemies:
            enemy.spawn(screen)
            if not PAUSE_STATE:
                enemy.move()

            if current_time - enemy.health_bar_time <= HEALTH_BAR_DELAY:
                enemy.draw_health_bar(screen)
                
            if current_time - enemy.explosion_time <= EXPLOSION_DELAY:
                screen.blit(explode_img, (enemy.x+(enemy.width)//2-12, enemy.y+(enemy.width)//2-12))

            if current_time - enemy.crash_time <= EXPLOSION_DELAY:
                screen.blit(blast_img, (enemy.x+(enemy.width)//2-32, enemy.y+enemy.width-24))

            if (current_time - enemy.last_slime_time >= SLIME_DELAY) and (current_time - enemy.spawn_time >= SLIME_DELAY) and not PAUSE_STATE:
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
            if current_time - defeat.defeat_time <= EXPLOSION_DELAY:
                screen.blit(explode2_img, (defeat.x+(defeat.width)//2-32, defeat.y+(defeat.width)//2-32))
            else:
                defeated.remove(defeat)

        for bullet in bullets:
            bullet.draw(screen)
            if not PAUSE_STATE:
                bullet.move()
            for enemy in enemies:
                if math.sqrt(math.pow((bullet.x+12-(enemy.x+(enemy.width/2)/2)), 2)+math.pow((bullet.y-(enemy.y+enemy.width/2)), 2)) < enemy.width/2:
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
                        PLAYER_SCORE += enemy.max_health
                        if enemy.isBoss:
                            ENEMY_COUNT = 0
                            GAME_LEVEL += 1
                            SLIME_DELAY = 500 if SLIME_DELAY < 1000 else SLIME_DELAY - 500
                            SPAWN_DELAY = 500 if SPAWN_DELAY < 1000 else SPAWN_DELAY - 500
                            FIRE_DELAY -= (GAME_LEVEL-1)*10
                            player.health = 100 + (GAME_LEVEL - 1) * 10
                            player.max_health = 100 + (GAME_LEVEL - 1) * 10
                            player.health_bar_time = current_time
                            LEVEL_BANNER_TIME = current_time
                            ENEMY_SPEED += 0.1
                            BOSS_SPEED -= 0.05
                            slimes.clear()
                        enemies.remove(enemy)

            if (bullet in bullets) and (bullet.y < 0):
                bullets.remove(bullet) 

        for slime in slimes:
            slime.draw(screen)
            if not PAUSE_STATE:
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
            if GAME_LEVEL < 6:
                player.draw(screen)
                if not PAUSE_STATE:
                    player.move()

                if current_time - LEVEL_BANNER_TIME <= LEVEL_DELAY:
                    level_banner_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
                    screen.blit(level_banner, level_banner_rect)
                    if not JUST_SPAWNED:
                        screen.blit(health_restored, health_restored_rect)

                if current_time - player.health_bar_time <= HEALTH_BAR_DELAY:
                    player.draw_health_bar(screen)

                if current_time - player.explosion_time <= EXPLOSION_DELAY:
                    screen.blit(explode_img, (player.x+(PLAYER_WIDTH)//2-12, player.y+(PLAYER_WIDTH)//2-12))

                if current_time - player.crash_time <= CRASH_DELAY:
                    player.y += 10 

                if not (current_time - LEVEL_BANNER_TIME <= LEVEL_DELAY):
                    screen.blit(level_indicator,(10, 10))
                    score_indicator_rect.topright = (SCREEN_WIDTH-10, 10)
                    screen.blit(score_indicator, score_indicator_rect)

                if current_time - PLAY_TIME <= PLAY_DELAY and not (current_time - LEVEL_BANNER_TIME <= LEVEL_DELAY):
                    play()

                if PAUSE_STATE:
                    pause()
            else:
                you_win()
        else:
            gameover()
            score_indicator_rect.center = (SCREEN_WIDTH//2, (SCREEN_HEIGHT//2) + 250)
            screen.blit(score_indicator, score_indicator_rect)

        pygame.display.update()