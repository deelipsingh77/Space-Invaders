import pygame
import random

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

enemyImg = pygame.image.load("assets/alien.png")
enemies = []
destroyed = True
last_spawn_time = 0
spawn_delay = 2000

bulletImg = pygame.image.load("assets/bullet.png")
fire = False
fire_delay = 200
bullets = []
last_shot_time = 0

def player(x, y):
    screen.blit(playerImg, (x, y))
    
class Enemy:
    def __init__(self):
        self.x = random.randint(0, 800-64)
        self.y = random.randint(30, 300-64-30)
        self.x_change = 0.3
        self.y_change = 40

    def spawn(self):
        screen.blit(enemyImg, (self.x, self.y))

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
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5

    def fire_bullet(self):
        screen.blit(bulletImg, (self.x+32-12, self.y-15))

    def move(self):
        self.y -= self.speed


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

    if destroyed or ((current_time - last_spawn_time) >= spawn_delay):
        enemy_spawn = Enemy()
        enemies.append(enemy_spawn)
        destroyed = False
        last_spawn_time = current_time

    for enemy in enemies:
        enemy.spawn()
        enemy.move() 

    if playerX < 0:
        playerX = 0
    elif playerX > 800-64:
        playerX = 800-64

    if playerY < 0:
        playerY = 0
    elif playerY > 600-64:
        playerY = 600-64

    if fire and (current_time - last_shot_time) >= fire_delay:
        new_bullet = Bullet(playerX, playerY)
        bullets.append(new_bullet)
        last_shot_time = current_time

    for bullet in bullets:
        bullet.fire_bullet()
        bullet.move()
        for enemy in enemies:
            if ((bullet.x >= enemy.x-32 and bullet.x <= enemy.x+64-24) and (bullet.y < enemy.y+64)):
                bullets.pop(0)
                enemies.pop(0)
                # destroyed = True
            elif (bullet.y < -24):
                try:
                    bullets.pop(0) 
                except IndexError:
                    print("Popped from empty list")

    player(playerX, playerY)
    pygame.display.update()
