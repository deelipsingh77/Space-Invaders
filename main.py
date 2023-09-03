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
FIRE_DELAY = 100

#Initialize pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)

background = pygame.image.load("assets/space.jpg")

playerImg = pygame.image.load("assets/spaceship.png")
playerX = (800-64)/2
playerY = 600-64-30
playerX_change = 0
playerY_change = 0
crashed = False

enemyImg = pygame.image.load("assets/alien.png")
bossImg = pygame.image.load("assets/monster.png")
enemies = []
destroyed = True
last_spawn_time = 0
spawn_delay = 5000
enemy_count = 0

bulletImg = pygame.image.load("assets/bullet.png")
fire = False
fire_delay = 100
bullets = []
last_shot_time = 0

slimeImg = pygame.image.load("assets/slime.png")
slimes = []

gameoverImg = pygame.image.load("assets/gameover.png")

def player(x, y):
    screen.blit(playerImg, (x, y))

def gameover():
    global fire, playerX, playerY, enemy_count
    enemy_count = 0
    screen.blit(gameoverImg, ((800-600)/2, (600-309)/2))
    enemies.clear()
    fire = False
    screen.blit(text_surface,text_rect.topleft)
    playerX = (800-64)/2
    playerY = 600-64-30
    slimes.clear()
    
class Enemy:
    def __init__(self):
        self.height = 64
        self.width = 64
        self.x = random.randint(0, 800-64)
        self.y = -self.height
        self.x_change = 0.3
        self.y_change = 0.3
        self.last_slime_time = 0
        self.spawn_time = 0
        self.h_move = False
        self.v_move = True
        self.start = -10
        self.health = 100
        self.isBoss = False

    def spawn(self):
        if not self.isBoss:
            screen.blit(enemyImg, (self.x, self.y))
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
            self.x_change = 0.3
        elif self.x > 800-64:
            self.x = 800-64
            self.v_move = True
            self.h_move = False
            self.x_change = -0.3

class Bullet:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def fire_bullet(self, image):
        screen.blit(image, (self.x+32-12, self.y-15))

    def move_bullet(self):
        self.y -= self.speed

    def move_slime(self):
        self.y += self.speed

font = pygame.font.Font(None, 36)
text_surface = font.render("Press Spacebar to Play Again!", True, (255,255,255))
text_rect = text_surface.get_rect()
text_rect.center = (800//2, (600//2)+200)

running  = True
while running:
    #Background Color    
    # screen.fill((0, 0, 0))

    current_time = pygame.time.get_ticks()

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_UP:
                playerY_change = -1
            if event.key == pygame.K_DOWN:
                playerY_change = 1
            if event.key == pygame.K_SPACE:
                if crashed:
                    crashed = False
                else:
                    fire = True

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                playerX_change = 0
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                playerY_change = 0
            elif event.key == pygame.K_SPACE:
                fire = False


    playerX += playerX_change
    playerY += playerY_change

    if (destroyed or ((current_time - last_spawn_time) >= spawn_delay)) and not crashed:
        if enemy_count < 5:
            enemy_spawn = Enemy()
            enemy_spawn.height = 64
            enemy_spawn.width = 64
            enemies.append(enemy_spawn)
            destroyed = False
            last_spawn_time  = current_time
            enemy_spawn.spawn_time = current_time
            enemy_count += 1
        elif enemy_count == 5:
            enemy_spawn = Enemy()
            enemy_spawn.height = 128
            enemy_spawn.width = 128
            enemy_spawn.y_change = 0.1
            enemy_spawn.isBoss = True
            enemy_spawn.health = 1000
            enemies.append(enemy_spawn)
            last_spawn_time  = current_time
            enemy_spawn.spawn_time = current_time
            enemy_count += 1

    for enemy in enemies:
        enemy.spawn()
        enemy.move()
        if (current_time - enemy.last_slime_time > 3000) and (current_time - enemy.spawn_time > 3000):
            new_slime = Bullet(enemy.x, enemy.y+48, 1)
            slimes.append(new_slime)
            enemy.last_slime_time = current_time
        if math.sqrt(math.pow((enemy.x-playerX), 2)+math.pow((enemy.y-playerY), 2)) < 40:
            crashed = True

        if playerX < 0:
            playerX = 0
        elif playerX > 800-64:
            playerX = 800-64

        if playerY < 0:
            playerY = 0
        elif playerY > 600-64:
            playerY = 600-64

    if fire and (current_time - last_shot_time) >= fire_delay:
        new_bullet = Bullet(playerX, playerY, 5)
        bullets.append(new_bullet)
        last_shot_time = current_time

    for bullet in bullets:
        bullet.fire_bullet(bulletImg)
        bullet.move_bullet()
        for enemy in enemies:
            if math.sqrt(math.pow((bullet.x+12-(enemy.x+(enemy.width/2)/2)), 2)+math.pow((bullet.y-(enemy.y+enemy.width/2)), 2)) < enemy.width/2:
                enemy.health -= 10
                bullets.pop(bullets.index(bullet))
                if enemy.health == 0:
                    enemies.pop(enemies.index(enemy))
                elif enemy.health == 0 and enemy.isBoss:
                    enemy_count = 0 
                    enemies.pop(enemies.index(enemy))

        if (bullet in bullets) and (bullet.y < 0):
            bullets.pop(bullets.index(bullet)) 

    for slime in slimes:
        slime.fire_bullet(slimeImg)
        slime.move_slime()
        if (math.sqrt(math.pow((slime.x+12-playerX+32), 2)+math.pow((slime.y-playerY+32), 2))) < 30:
            crashed = True

        if slime.y > 600:
            slimes.pop(slimes.index(slime))

    if not crashed:
        player(playerX, playerY)
    else:
        gameover()

    pygame.display.update()
