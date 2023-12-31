import sys
import core.states as states
import graphics.assets as assets
from core.constants import SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_HEIGHT, PLAYER_WIDTH
from graphics.damage import damage_display
from graphics.texts import level_display, hud_display 
from core.states import play, pause, gameover
from graphics.healthbar import health_bar_display

class Player:
    CRASH_DELAY = 100
    PLAYER_SPEED = 5

    def __init__(self):
        self.isPlayer = True
        self.rect = assets.images['spaceship_img'].get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT-PLAYER_HEIGHT))
        self.height = PLAYER_HEIGHT
        self.width = PLAYER_WIDTH
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
        screen.blit(assets.images['spaceship_img'], self.rect)

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
        if not states.GAME_OVER:
            if states.GAME_LEVEL < 6:
                player.draw(screen)
                if not states.PAUSE_STATE:
                    player.move()

                health_bar_display(screen, player, current_time)
                level_display(screen, current_time)
                damage_display(screen, player, current_time)

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
                gameover(screen, player, enemies, bullets, slimes, defeated)
        else:
            gameover(screen, player, enemies, bullets, slimes, defeated)