import pygame
import sys
import states
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_HEIGHT, PLAYER_WIDTH
from assets import spaceship_img, explode_img
from texts import level_display, hud_display 
from states import play, pause, gameover

class Player:
    CRASH_DELAY = 100
    PLAYER_SPEED = 5

    def __init__(self):
        self.rect = spaceship_img.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT-PLAYER_HEIGHT))
        self.x_change = 0
        self.y_change = 0
        self.max_health = 100
        self.health = self.max_health
        self.explosion_time = sys.float_info.min
        self.defeat_time = sys.float_info.min
        self.crash_time = sys.float_info.min
        self.health_bar_time = sys.float_info.min

    def move(self):
        self.rect.centerx += self.x_change
        self.rect.centery += self.y_change
        self.rect.right = SCREEN_WIDTH if self.rect.right > SCREEN_WIDTH else self.rect.right
        self.rect.left = 0 if self.rect.left < 0 else self.rect.left
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = SCREEN_HEIGHT if self.rect.bottom > SCREEN_HEIGHT else self.rect.bottom

    def draw(self, screen):
        screen.blit(spaceship_img, self.rect)
    
    def draw_health_bar(self, screen):
        bar_width = PLAYER_WIDTH
        bar_height = 5
        GRAY = (80, 80, 80)
        RED = (180, 0, 0)
        GREEN = (0, 180, 100)
        if (self.health / self.max_health)*100 < 25:
            COLOR = RED
        else:
            COLOR = GREEN
        
        health_width = (self.health / self.max_health) * bar_width
        if self.health != self.max_health:
            pygame.draw.rect(screen, GRAY, (self.rect.left, self.rect.bottom + 10, bar_width, bar_height))
            pygame.draw.rect(screen, COLOR, (self.rect.left, self.rect.bottom + 10, health_width, bar_height))

    def move_left(self):
        self.x_change = -Player.PLAYER_SPEED
    def move_right(self):
        self.x_change = Player.PLAYER_SPEED
    def move_up(self):
        self.y_change = -Player.PLAYER_SPEED
    def move_down(self):
        self.y_change = Player.PLAYER_SPEED

    def stop_x(self):
        self.x_change = 0
    def stop_y(self):
        self.y_change = 0

    @staticmethod
    def update_player(screen, player, current_time, enemies, bullets, slimes, defeated):
        if player.health > 0:
            if states.GAME_LEVEL < 6:
                player.draw(screen)
                if not states.PAUSE_STATE:
                    player.move()

                if current_time - states.LEVEL_BANNER_TIME <= states.LEVEL_DELAY:
                    level_display(screen)

                if current_time - player.health_bar_time <= states.HEALTH_BAR_DELAY:
                    player.draw_health_bar(screen)

                if current_time - player.explosion_time <= states.EXPLOSION_DELAY:
                    explode_img_rect = explode_img.get_rect(center = player.rect.center)
                    screen.blit(explode_img, explode_img_rect)

                if current_time - player.crash_time <= Player.CRASH_DELAY:
                    player.rect.top += 20 

                if not (current_time - states.LEVEL_BANNER_TIME <= states.LEVEL_DELAY):
                    hud_display(screen)
                if current_time - states.PLAY_TIME <= states.PLAY_DELAY and not (current_time - states.LEVEL_BANNER_TIME <= states.LEVEL_DELAY):
                    play(screen)

                if states.PAUSE_STATE:
                    pause(screen)
            else:
                states.WIN_STATE = True
                gameover(screen, enemies, bullets, slimes, defeated)
        else:
            gameover(screen, enemies, bullets, slimes, defeated)