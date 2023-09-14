import core.states as states
import core.constants as constants
from entities.bullet import Bullet
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_RETURN, K_ESCAPE, K_SPACE
from core.states import toggle_pause, reset

def return_action(player, *entities):
    if not states.PAUSE_STATE:
        reset(player, *entities)
    else:
        if constants.pause_option:
            states.PAUSE_STATE = False
        else:
            reset(player, *entities)
            constants.MENU_STATE = True
            
def up_action(player):
    if not states.PAUSE_STATE:
        player.move_up()
    else:
        if constants.pause_option:
            constants.pause_option = False
        else:
            constants.pause_option = True

def down_action(player):
    if not states.PAUSE_STATE:
        player.move_down()
    else:
        if constants.pause_option:
            constants.pause_option = False
        else:
            constants.pause_option = True

def handle_keydown_event(key, player, current_time, *entities):
    key_actions = {
        K_LEFT: lambda: player.move_left(),
        K_RIGHT: lambda: player.move_right(),
        K_UP: lambda: up_action(player),
        K_DOWN: lambda: down_action(player),
        K_RETURN: lambda: return_action(player, *entities),
        K_ESCAPE: lambda: toggle_pause(player, current_time),
        K_SPACE: lambda: Bullet.fire(player, *entities)
    }
    action = key_actions.get(key)
    if action:
        action()

def handle_keyup_event(key, player):
    key_actions = {
        K_LEFT: lambda: player.stop_x(),
        K_RIGHT: lambda: player.stop_x(),
        K_UP: lambda: player.stop_y(),
        K_DOWN: lambda: player.stop_y(),
        K_SPACE: lambda: Bullet.hold_fire()
    }

    action = key_actions.get(key)
    if action:
        action()