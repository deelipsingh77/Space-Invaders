import pygame
import random
import math

#Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 64
PLAYER_HEIGHT = 64
BOSS_WIDTH = 128
BOSS_HEIGHT = 128
ENEMY_SPAWN_DELAY = 5000
FIRE_DELAY = 0
LAST_SHOT_TIME = 0
LAST_SPAWN_TIME = 0
ENEMY_COUNT = 0
JUST_SPAWNED = True
SPAWN_DELAY = 5000
ENEMY_COUNT = 0
GAME_OVER = False
LEVEL = 1
ENEMY_SPEED = 0.3
BOSS_SPEED = 0.2
SCORE = 0

#Initialize pygame
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)

background = pygame.image.load("assets/space.jpg")
playerImg = pygame.image.load("assets/spaceship.png")
enemyImg = [pygame.image.load("assets/alien.png"), pygame.image.load("assets/ufo.png")]
bossImg = pygame.image.load("assets/monster.png")
bulletImg = pygame.image.load("assets/bullet.png")
slimeImg = pygame.image.load("assets/slime.png")
gameoverImg = pygame.image.load("assets/gameover.png")


class Player:
    def __init__(self):
        self.image = playerImg
        self.x = (SCREEN_WIDTH - PLAYER_WIDTH) / 2
        self.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 30
        self.x_change = 0
        self.y_change = 0
        self.crashed = False

    def move(self):
        self.x += self.x_change
        self.y += self.y_change
        self.x = max(0, min(SCREEN_WIDTH - PLAYER_WIDTH, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - PLAYER_HEIGHT, self.y))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

player = Player()

def gameover():
    global ENEMY_COUNT, GAME_OVER
    ENEMY_COUNT = 0
    screen.blit(gameoverImg, ((SCREEN_WIDTH-SCREEN_HEIGHT)/2, (SCREEN_HEIGHT-309)/2))
    enemies.clear()
    screen.blit(text_surface,text_rect.topleft)
    player.x = (SCREEN_WIDTH-PLAYER_WIDTH)/2
    player.y = (SCREEN_HEIGHT-PLAYER_HEIGHT)-30
    slimes.clear()
    GAME_OVER = True
    
class Enemy:
    def __init__(self):
        self.height = 64
        self.width = 64
        self.x = random.randint(0, SCREEN_HEIGHT - 64)
        self.y = -self.height
        self.x_change = ENEMY_SPEED
        self.y_change = ENEMY_SPEED
        self.last_slime_time = 0
        self.spawn_time = 0
        self.h_move = False
        self.v_move = True
        self.start = -10
        self.health = 100
        self.isBoss = False
        self.enemy = random.choice(enemyImg)

    def spawn(self):
        if not self.isBoss:
            screen.blit(self.enemy, (self.x, self.y))
        else:
            screen.blit(bossImg, (self.x, self.y))

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
            self.x_change = ENEMY_SPEED
        elif self.x > SCREEN_WIDTH-self.width:
            self.x = SCREEN_WIDTH-self.width
            self.v_move = True
            self.h_move = False
            self.x_change = -ENEMY_SPEED

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


font = pygame.font.Font(None, 36)
text_surface = font.render("Press Spacebar to Play Again!", True, (255,255,255))
text_rect = text_surface.get_rect()
text_rect.center = (SCREEN_WIDTH//2, (SCREEN_HEIGHT//2)+200)

font2 = pygame.font.Font(None, 30)

enemies = []
bullets = []
slimes = []

running  = True
while running:
    #Background Color    
    # screen.fill((0, 0, 0))

    current_time = pygame.time.get_ticks()

    level_indicator = font2.render(f"Level: {LEVEL}", True, (255,255,255))
    score_indicator = font2.render(f"Score: {SCORE}", True, (255,255,255))
    score_indicator_rect = score_indicator.get_rect()
    screen.blit(background, (0, 0))

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
                if player.crashed:
                    player.crashed = False
                    GAME_OVER = False
                else:
                    if current_time - LAST_SHOT_TIME >= FIRE_DELAY and not GAME_OVER:
                        new_bullet = Bullet(player.x, player.y)
                        bullets.append(new_bullet)
                        LAST_SHOT_TIME = current_time

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player.x_change = 0
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                player.y_change = 0

    if (JUST_SPAWNED or ((current_time - LAST_SPAWN_TIME) >= SPAWN_DELAY)) and not player.crashed:
        if ENEMY_COUNT < 5*LEVEL:
            enemy_spawn = Enemy()
            enemy_spawn.height = 64
            enemy_spawn.width = 64
            enemies.append(enemy_spawn)
            JUST_SPAWNED = False
            LAST_SPAWN_TIME  = current_time
            enemy_spawn.spawn_time = current_time
            ENEMY_COUNT += 1
        elif ENEMY_COUNT == 5*LEVEL:
            enemy_spawn = Enemy()
            enemy_spawn.height = 128
            enemy_spawn.width = 128
            enemy_spawn.y_change = BOSS_SPEED
            enemy_spawn.isBoss = True
            enemy_spawn.health = 1000
            enemies.append(enemy_spawn)
            LAST_SPAWN_TIME  = current_time
            enemy_spawn.spawn_time = current_time
            ENEMY_COUNT += 1

    for enemy in enemies:
        enemy.spawn()
        enemy.move()
        if (current_time - enemy.last_slime_time > 3000) and (current_time - enemy.spawn_time > 3000):
            new_slime = Slime(enemy.x, enemy.y+48, enemy.width)
            slimes.append(new_slime)
            enemy.last_slime_time = current_time
        if math.sqrt(math.pow((enemy.x-player.x), 2)+math.pow((enemy.y-player.y), 2)) < 40:
            player.crashed = True

    for bullet in bullets:
        bullet.draw()
        bullet.move()
        for enemy in enemies:
            if math.sqrt(math.pow((bullet.x+12-(enemy.x+(enemy.width/2)/2)), 2)+math.pow((bullet.y-(enemy.y+enemy.width/2)), 2)) < enemy.width/2:
                enemy.health -= 10
                bullets.remove(bullet)
                if enemy.health <= 0:
                    enemies.remove(enemy)
                    SCORE += 100
                    if enemy.isBoss:
                        ENEMY_COUNT = 0
                        LEVEL += 1 
                        ENEMY_SPEED += 0.2
                        BOSS_SPEED += 0.1 
                        SCORE += 900

        if (bullet in bullets) and (bullet.y < 0):
            bullets.remove(bullet) 

    for slime in slimes:
        slime.move()
        slime.draw()
        if (math.sqrt(math.pow((slime.x-player.x), 2)+math.pow((slime.y-player.y-24), 2))) < 37 and slime.enemy_width == PLAYER_WIDTH:
            player.crashed = True
        elif (math.sqrt(math.pow((slime.x-player.x), 2)+math.pow((slime.y-player.y-35), 2))) < 50 and slime.enemy_width == BOSS_WIDTH:
            player.crashed = True

        if slime.y > SCREEN_HEIGHT:
            slimes.remove(slime)

    if not player.crashed:
        player.move()
        player.draw()
        screen.blit(level_indicator,(10, 10))
        score_indicator_rect.topright = (SCREEN_WIDTH-10, 10)
        screen.blit(score_indicator, score_indicator_rect)
    else:
        gameover()
        score_indicator_rect.center = (SCREEN_WIDTH//2, (SCREEN_HEIGHT//2) + 250)
        screen.blit(score_indicator, score_indicator_rect)


    pygame.display.update()
