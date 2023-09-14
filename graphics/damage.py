import core.states as states
import graphics.assets as assets

def damage_display(screen, entity, current_time):
    if current_time - entity.explosion_time <= states.EXPLOSION_DELAY:
        explode_img_rect = assets.images['explode_img'].get_rect(center = entity.rect.center)
        screen.blit(assets.images['explode_img'], explode_img_rect)
        
def explosion_display(screen, entity, current_time):
    if current_time - entity.crash_time <= states.EXPLOSION_DELAY:
                blast_img_rect = assets.images['blast_img'].get_rect(midtop = entity.rect.midbottom)
                screen.blit(assets.images['blast_img'], blast_img_rect)