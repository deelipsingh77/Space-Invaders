import pygame
import random
import math
import sys

#Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 64
PLAYER_HEIGHT = 64
BOSS_WIDTH = 128
BOSS_HEIGHT = 128
LAST_SHOT_TIME = 0
LAST_SPAWN_TIME = 0
LEVEL_BANNER_TIME = 0
ENEMY_COUNT = 0
JUST_SPAWNED = True
FIRE_DELAY = 0
LEVEL_DELAY = 3000
SPAWN_DELAY = 5000
EXPLOSION_DELAY = 100
CRASH_DELAY = 100
HEALTH_BAR_DELAY = 3000
SLIME_DELAY = 3000
STAR_DELAY = 3000
ENEMY_COUNT = 0
LEVEL = 1
ENEMY_SPEED = 0.3
BOSS_SPEED = 0.3
STAR_SPEED = 0.03
SCORE = 0
STAR_GENERATION_TIME = 0
COLORS = [(255, 255, 255), (255, 255, 200), (255, 225, 150)]

#Initialize pygame
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)

playerImg = pygame.image.load("assets/spaceship.png")
enemyImg = [pygame.image.load("assets/alien.png"), pygame.image.load("assets/ufo.png"), pygame.image.load("assets/monster2.png")]
bossImg = [pygame.image.load("assets/monster.png"), pygame.image.load("assets/santelmo.png"), pygame.image.load("assets/alien2.png"), pygame.image.load("assets/kraken.png"), pygame.image.load("assets/cthulhu.png")]
bulletImg = pygame.image.load("assets/bullet.png")
slimeImg = pygame.image.load("assets/slime.png")
gameoverImg = pygame.image.load("assets/gameover.png")
youwinImg = pygame.image.load("assets/you-win.png")
explodeImg = pygame.image.load("assets/explode.png")
explodeImg2 = pygame.image.load("assets/explode2.png")
blastingImg = pygame.image.load("assets/blasting.png")

class Player:
    def __init__(self):
        self.image = playerImg
        self.x = (SCREEN_WIDTH - PLAYER_WIDTH) / 2
        self.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 30
        self.x_change = 0
        self.y_change = 0
        self.max_health = 100
        self.health = self.max_health
        self.explosion_time = sys.float_info.min
        self.defeat_time = sys.float_info.min
        self.crash_time = sys.float_info.min
        self.health_bar_time = sys.float_info.min
        self.width = PLAYER_WIDTH

    def move(self):
        self.x += self.x_change
        self.y += self.y_change
        self.x = max(0, min(SCREEN_WIDTH - PLAYER_WIDTH, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - PLAYER_HEIGHT, self.y))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
    
    def draw_health_bar(self):
        bar_width = player.width
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
            pygame.draw.rect(screen, GRAY, (self.x, self.y + PLAYER_HEIGHT + 10, bar_width, bar_height))
            pygame.draw.rect(screen, COLOR, (self.x, self.y + PLAYER_HEIGHT + 10, health_width, bar_height))

player = Player()

class Enemy:
    def __init__(self, isBoss):
        self.isBoss = isBoss
        if self.isBoss:
            self.height = 128
            self.width = 128
            self.x_change = BOSS_SPEED
            self.y_change = BOSS_SPEED
            self.max_health = 1000*LEVEL
            self.health = self.max_health
        else:
            self.x_change = ENEMY_SPEED
            self.y_change = ENEMY_SPEED
            self.height = 64
            self.width = 64
            self.max_health = 100+(LEVEL-1)*10
            self.health = self.max_health
        self.x = random.randint(0, SCREEN_WIDTH - 128)
        self.y = -self.height
        self.last_slime_time = 0
        self.spawn_time = 0
        self.h_move = False
        self.v_move = True
        self.start = -10
        self.enemy = random.choice(enemyImg)
        self.explosion_time = sys.float_info.min
        self.defeat_time = sys.float_info.min
        self.crash_time = sys.float_info.min
        self.health_bar_time = sys.float_info.min

    def spawn(self):
        if not self.isBoss:
            screen.blit(self.enemy, (self.x, self.y))
        else:
            screen.blit(bossImg[LEVEL-1], (self.x, self.y))

    def move(self):
        if self.v_move:
            self.y += self.y_change
            if round(self.y - self.start) > 70:
                self.v_move = False
                self.h_move = True
                self.start = self.y
        elif self.h_move:
            self.x += self.x_change

        if self.x < 0:
            self.x = 0
            self.v_move = True
            self.h_move = False
            if self.isBoss:
                self.x_change = BOSS_SPEED
            else:
                self.x_change = ENEMY_SPEED
        elif self.x > SCREEN_WIDTH-self.width:
            self.x = SCREEN_WIDTH-self.width
            self.v_move = True
            self.h_move = False
            if self.isBoss:
                self.x_change = -BOSS_SPEED
            else:
                self.x_change = -ENEMY_SPEED
    
    def draw_health_bar(self):
        bar_width = enemy.width
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
            pygame.draw.rect(screen, GRAY, (self.x, self.y-10, bar_width, bar_height))
            pygame.draw.rect(screen, COLOR, (self.x, self.y-10, health_width, bar_height))

class Bullet:
    def __init__(self, x, y):
        self.image = bulletImg
        self.x = x
        self.y = y
        self.speed = 5

    def draw(self):
        screen.blit(self.image, (self.x + 32 - 12, self.y - 15))

    def move(self):
        self.y -= self.speed

class Slime:
    def __init__(self, x, y, enemy_width):
        self.image = slimeImg
        self.x = x
        self.y = y
        self.speed = 1
        self.enemy_width = enemy_width

    def move(self):
        self.y += self.speed

    def draw(self):
        if self.enemy_width == PLAYER_WIDTH:
            screen.blit(self.image, (self.x + self.enemy_width/2 - 12, self.y - 12))
        else:
            screen.blit(self.image, (self.x + self.enemy_width/2 - 30, self.y - 12))
            screen.blit(self.image, (self.x + self.enemy_width/2 - 12, self.y - 12))
            screen.blit(self.image, (self.x + self.enemy_width/2 + 6, self.y - 12))
        
class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.size = random.randint(1, 4)
        self.y = -self.size
        self.speed = random.uniform(0.01, 0.02) if self.size < 2 else STAR_SPEED
        self.color = random.choice(COLORS)
    
    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

font = pygame.font.Font(None, 36)
text_surface = font.render("Press Spacebar to Play Again!", True, (255,255,255))
text_rect = text_surface.get_rect()
text_rect.center = (SCREEN_WIDTH//2, (SCREEN_HEIGHT//2)+200)

font2 = pygame.font.Font(None, 30)
font3 = pygame.font.Font(None, 200)
health_restored = font2.render("Health Restored! Max Health + 10", True, (255, 255, 255))
health_restored_rect = health_restored.get_rect()
health_restored_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100)

def gameover():
    screen.blit(gameoverImg, ((SCREEN_WIDTH-600)//2, (SCREEN_HEIGHT-309)//2))
    screen.blit(text_surface,text_rect.topleft)
    player.x = (SCREEN_WIDTH-PLAYER_WIDTH)/2
    player.y = (SCREEN_HEIGHT-PLAYER_HEIGHT)-30
    enemies.clear()
    slimes.clear()
    bullets.clear()
    defeated.clear()
    reset()

def you_win():
    screen.blit(youwinImg, ((SCREEN_WIDTH-256)//2, (SCREEN_HEIGHT-256)//2))
    screen.blit(text_surface,text_rect.topleft)
    player.x = (SCREEN_WIDTH-PLAYER_WIDTH)/2
    player.y = (SCREEN_HEIGHT-PLAYER_HEIGHT)-30
    enemies.clear()
    slimes.clear()
    bullets.clear()
    defeated.clear()
    reset()


def reset():
    global SPAWN_DELAY, FIRE_DELAY, LAST_SHOT_TIME, LAST_SPAWN_TIME, ENEMY_COUNT, JUST_SPAWNED, EXPLOSION_DELAY, CRASH_DELAY, HEALTH_BAR_DELAY, SLIME_DELAY, SLIME_DELAY, LEVEL, ENEMY_SPEED, BOSS_SPEED, SCORE

    SPAWN_DELAY = 5000
    FIRE_DELAY = 0
    LAST_SHOT_TIME = 0
    LAST_SPAWN_TIME = 0
    ENEMY_COUNT = 0
    JUST_SPAWNED = True
    EXPLOSION_DELAY = 100
    CRASH_DELAY = 100
    HEALTH_BAR_DELAY = 3000
    SLIME_DELAY = 3000
    ENEMY_COUNT = 0
    LEVEL = 1
    ENEMY_SPEED = 0.3
    BOSS_SPEED = 0.2
    SCORE = 0

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

running  = True
while running:
    #Background Color    
    screen.fill((0, 0, 0))

    current_time = pygame.time.get_ticks()

    level_indicator = font2.render(f"Level: {LEVEL}", True, (255,255,255))
    level_banner = font3.render(f"Level {LEVEL}", True, (255,255,255))
    level_banner_rect = level_banner.get_rect()
    score_indicator = font2.render(f"Score: {SCORE}", True, (255,255,255))
    score_indicator_rect = score_indicator.get_rect()

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
            if event.key == pygame.K_SPACE:
                if player.health <= 0:
                    player.health = 100
                elif LEVEL > 5:
                    reset()
                else:
                    if current_time - LAST_SHOT_TIME >= FIRE_DELAY and not player.health == 0:
                        new_bullet = Bullet(player.x, player.y)
                        bullets.append(new_bullet)
                        LAST_SHOT_TIME = current_time

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player.x_change = 0
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                player.y_change = 0

    if (JUST_SPAWNED or ((current_time - LAST_SPAWN_TIME) >= SPAWN_DELAY)) and not player.health <= 0 and not (current_time - LEVEL_BANNER_TIME <= LEVEL_DELAY):
        if ENEMY_COUNT < 5*LEVEL:
            enemy_spawn = Enemy(False)
            enemies.append(enemy_spawn)
            JUST_SPAWNED = False
            LAST_SPAWN_TIME  = current_time
            enemy_spawn.spawn_time = current_time
            ENEMY_COUNT += 1
        elif ENEMY_COUNT == 5*LEVEL:
            enemy_spawn = Enemy(True)
            enemies.append(enemy_spawn)
            LAST_SPAWN_TIME  = current_time
            enemy_spawn.spawn_time = current_time
            ENEMY_COUNT += 1
    
    if current_time - STAR_GENERATION_TIME >= STAR_DELAY and not player.health <= 0:
        count = random.randint(3, 5)
        for i in range(count):
            new_star = Star()
            stars.append(new_star)
            STAR_GENERATION_TIME = current_time
    
    for star in stars:
        star.draw()
        star.move()

        if star.y > SCREEN_HEIGHT:
            stars.remove(star)

    for enemy in enemies:
        enemy.spawn()
        enemy.move()
        if current_time - enemy.health_bar_time <= HEALTH_BAR_DELAY:
            enemy.draw_health_bar()
            
        if current_time - enemy.explosion_time <= EXPLOSION_DELAY:
            screen.blit(explodeImg, (enemy.x+(enemy.width)//2-12, enemy.y+(enemy.width)//2-12))

        if current_time - enemy.crash_time <= EXPLOSION_DELAY:
            screen.blit(blastingImg, (enemy.x+(enemy.width)//2-32, enemy.y+enemy.width-24))

        if (current_time - enemy.last_slime_time >= SLIME_DELAY) and (current_time - enemy.spawn_time >= SLIME_DELAY):
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
            screen.blit(explodeImg2, (defeat.x+(defeat.width)//2-32, defeat.y+(defeat.width)//2-32))
        else:
            defeated.remove(defeat)

    for bullet in bullets:
        bullet.draw()
        bullet.move()
        for enemy in enemies:
            if math.sqrt(math.pow((bullet.x+12-(enemy.x+(enemy.width/2)/2)), 2)+math.pow((bullet.y-(enemy.y+enemy.width/2)), 2)) < enemy.width/2:
                enemy.health -= 10
                enemy.explosion_time = current_time
                enemy.health_bar_time = current_time
                try:
                    bullets.remove(bullet)
                except ValueError:
                    pass
                if enemy.health <= 0:
                    enemy.defeat_time = current_time
                    defeated.append(enemy)
                    SCORE += enemy.max_health
                    if enemy.isBoss:
                        ENEMY_COUNT = 0
                        LEVEL += 1
                        SLIME_DELAY = 500 if SLIME_DELAY < 1000 else SLIME_DELAY - 500
                        SPAWN_DELAY = 500 if SPAWN_DELAY < 1000 else SPAWN_DELAY - 500
                        player.health = 100 + (LEVEL - 1) * 10
                        player.max_health = 100 + (LEVEL - 1) * 10
                        player.health_bar_time = current_time
                        LEVEL_BANNER_TIME = current_time
                        ENEMY_SPEED += 0.1
                        BOSS_SPEED -= 0.05 
                    enemies.remove(enemy)

        if (bullet in bullets) and (bullet.y < 0):
            bullets.remove(bullet) 

    for slime in slimes:
        slime.move()
        slime.draw()
        if (math.sqrt(math.pow((slime.x-player.x), 2)+math.pow((slime.y-player.y-24), 2))) < 37 and slime.enemy_width == PLAYER_WIDTH:
            slimes.remove(slime)
            player.health -= 10
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

    if not player.health == 0:
        if LEVEL < 6:
            player.move()
            player.draw()

            if current_time - LEVEL_BANNER_TIME <= LEVEL_DELAY:
                level_banner_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
                screen.blit(level_banner, level_banner_rect)
                if not JUST_SPAWNED:
                    screen.blit(health_restored, health_restored_rect)

            if current_time - player.health_bar_time <= HEALTH_BAR_DELAY:
                player.draw_health_bar()

            if current_time - player.explosion_time <= EXPLOSION_DELAY:
                screen.blit(explodeImg, (player.x+(PLAYER_WIDTH)//2-12, player.y+(PLAYER_WIDTH)//2-12))

            if current_time - player.crash_time <= CRASH_DELAY:
                player.y += 10 

            if not (current_time - LEVEL_BANNER_TIME <= LEVEL_DELAY):
                screen.blit(level_indicator,(10, 10))
                score_indicator_rect.topright = (SCREEN_WIDTH-10, 10)
                screen.blit(score_indicator, score_indicator_rect)
        else:
            you_win()
    else:
        gameover()
        score_indicator_rect.center = (SCREEN_WIDTH//2, (SCREEN_HEIGHT//2) + 250)
        screen.blit(score_indicator, score_indicator_rect)

    pygame.display.update()