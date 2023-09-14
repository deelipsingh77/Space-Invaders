import pygame
import core.states as states

def health_bar_display(screen, entity, current_time):
    if current_time - entity.health_bar_time <= states.HEALTH_BAR_DELAY:
        bar_width = entity.width
        bar_height = 5
        GRAY = (80, 80, 80)
        RED = (180, 0, 0)
        GREEN = (0, 180, 100)
        if (entity.health / entity.max_health)*100 < 25:
            COLOR = RED
        else:
            COLOR = GREEN
        
        health_width = (entity.health / entity.max_health) * bar_width
        if entity.health != entity.max_health:
            if entity.isPlayer:
                pygame.draw.rect(screen, GRAY, (entity.rect.left, entity.rect.bottom + 10, bar_width, bar_height))
                pygame.draw.rect(screen, COLOR, (entity.rect.left, entity.rect.bottom + 10, health_width, bar_height))
            else:
                pygame.draw.rect(screen, GRAY, (entity.rect.left, entity.rect.top - 10, bar_width, bar_height))
                pygame.draw.rect(screen, COLOR, (entity.rect.left, entity.rect.top - 10, health_width, bar_height))