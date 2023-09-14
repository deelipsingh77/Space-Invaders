import core.states as states
from entities.bullet import Bullet
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_RETURN, K_ESCAPE, K_SPACE
from core.states import toggle_pause, reset

def return_action(player, *entities):
    if not states.PAUSE_STATE:
        reset(player, entities[0], *entities)

def handle_keydown_event(key, player, current_time, *entities):
    key_actions = {
        K_LEFT: lambda: player.move_left(),
        K_RIGHT: lambda: player.move_right(),
        K_UP: lambda: player.move_up(),
        K_DOWN: lambda: player.move_down(),
        K_RETURN: lambda: return_action(player, *entities),
        K_ESCAPE: lambda: toggle_pause(player, current_time),
        K_SPACE: lambda: Bullet.fire(player, entities[0], *entities)
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