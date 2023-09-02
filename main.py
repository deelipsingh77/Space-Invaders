import pygame
import random
import math

#Initialize pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)

playerImg = pygame.image.load("assets/spaceship.png")
playerX = (800-64)/2
playerY = 600-64-30
playerX_change = 0
playerY_change = 0
crashed = False

enemyImg = pygame.image.load("assets/alien.png")
enemies = []
destroyed = True
last_spawn_time = 0
spawn_delay = 5000

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
    global fire, playerX, playerY
    screen.blit(gameoverImg, ((800-600)/2, (600-309)/2))
    enemies.clear()
    fire = False
    screen.blit(text_surface,text_rect.topleft)
    playerX = (800-64)/2
    playerY = 600-64-30
    slimes.clear()
    
class Enemy:
    def __init__(self):
        self.x = random.randint(0, 800-64)
        self.y = random.randint(30, 300-64-30)
        self.x_change = 0.3
        self.y_change = 40
        self.last_slime_time = 0
        self.spawn_time = 0

    def spawn(self):
        screen.blit(enemyImg, (self.x, self.y))
        self.move()

    def move(self):
        self.x += self.x_change
        if self.x < 0:
            self.x = 0
            self.y += self.y_change
            self.x_change = 0.3
        elif self.x > 800-64:
            self.x = 800-64
            self.y += self.y_change
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
    screen.fill((0, 0, 0))

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

    current_time = pygame.time.get_ticks()

    playerX += playerX_change
    playerY += playerY_change

    if (destroyed or ((current_time - last_spawn_time) >= spawn_delay)) and not crashed:
        enemy_spawn = Enemy()
        enemies.append(enemy_spawn)
        destroyed = False
        last_spawn_time  = current_time
        enemy_spawn.spawn_time = current_time

    for enemy in enemies:
        enemy.spawn()
        if (current_time - enemy.last_slime_time > 3000) and (current_time - enemy.spawn_time > 3000):
            new_slime = Bullet(enemy.x, enemy.y, 1)
            slimes.append(new_slime)
            enemy.last_slime_time = current_time


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
            if math.sqrt(math.pow((bullet.x-enemy.x), 2)+math.pow((bullet.y-enemy.y), 2)) < 30:
                bullets.pop(bullets.index(bullet))
                enemies.pop(enemies.index(enemy))

        if (bullet in bullets) and (bullet.y < 0):
            bullets.pop(bullets.index(bullet)) 

    for slime in slimes:
        slime.fire_bullet(slimeImg)
        slime.move_slime()
        if (math.sqrt(math.pow((slime.x-playerX), 2)+math.pow((slime.y-playerY), 2))) < 30:
            crashed = True

        if slime.y > 600:
            slimes.pop(slimes.index(slime))

    for enemy in enemies:
        if math.sqrt(math.pow((enemy.x-playerX), 2)+math.pow((enemy.y-playerY), 2)) < 40:
            crashed = True

    if not crashed:
        player(playerX, playerY)
    else:
        gameover()

    pygame.display.update()
