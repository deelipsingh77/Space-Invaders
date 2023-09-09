import states
from assets import explode_img

def damage_display(screen, entity, current_time):
    if current_time - entity.explosion_time <= states.EXPLOSION_DELAY:
        explode_img_rect = explode_img.get_rect(center = entity.rect.center)
        screen.blit(explode_img, explode_img_rect)