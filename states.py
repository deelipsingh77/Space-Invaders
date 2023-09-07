import attributes as atr
from texts import game_over_text, game_over_rect, game_win_text, game_win_rect
from assets import gameover_img, play_img, pause_img, youwin_img
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

def gameover(screen, player, enemies, slimes, bullets, defeated):
    screen.blit(gameover_img, ((SCREEN_WIDTH-600)//2, (SCREEN_HEIGHT-309)//2))
    screen.blit(game_over_text,game_over_rect)
    atr.reset(player, enemies, slimes, bullets, defeated)

def play(screen):
    screen.blit(play_img, ((SCREEN_WIDTH-128)//2, (SCREEN_HEIGHT-128)//2))

def pause(screen):
    screen.blit(pause_img, ((SCREEN_WIDTH-128)//2, (SCREEN_HEIGHT-128)//2))

def you_win(screen, player, enemies, slimes, bullets, defeated):
    screen.blit(youwin_img, ((SCREEN_WIDTH-256)//2, (SCREEN_HEIGHT-256)//2))
    screen.blit(game_win_text,game_win_rect)