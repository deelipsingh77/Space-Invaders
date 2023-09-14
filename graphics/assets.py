ICON_IMAGE_PATH = "assets/icon.png"
SPACESHIP_IMAGE_PATH = "assets/player/spaceship.png"
ENEMY_IMAGE_PATHS = ["assets/minions/alien.png", "assets/minions/ufo.png", "assets/minions/monster2.png"] 
BOSS_IMAGE_PATHS = ["assets/boss/monster.png", "assets/boss/santelmo.png", "assets/boss/alien2.png", "assets/boss/kraken.png", "assets/boss/cthulhu.png"]
BULLET_IMAGE_PATH = "assets/bullets/bullet.png"
SLIME_IMAGE_PATH = "assets/bullets/slime.png"
GAME_OVER_IMAGE_PATH = "assets/states/gameover.png"
YOU_WIN_IMAGE_PATH = "assets/states/you-win.png"
EXPLODE_IMAGE_PATH = "assets/bullets/explode.png"
EXPLODE_IMAGE_PATH2 = "assets/bullets/explode2.png"
BLASTING_IMAGE_PATH = "assets/bullets/blasting.png"
PLAY_IMAGE_PATH = "assets/states/play.png"
PAUSE_IMAGE_PATH = "assets/states/pause.png"

images = None
icon = None

def assign_assets(asset):
    global images, icon
    images = asset
    icon = images['icon_img']