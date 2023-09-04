class Slime:
    def __init__(self, x, y, enemy_width):
        self.image = slimeImg
        self.x = x
        self.y = y
        self.speed = 1
        self.enemy_width = enemy_width
        self.damage = 10+((LEVEL-1)/10)

    def move(self):
        self.y += self.speed

    def draw(self):
        if self.enemy_width == PLAYER_WIDTH:
            screen.blit(self.image, (self.x + self.enemy_width/2 - 12, self.y - 12))
        else:
            screen.blit(self.image, (self.x + self.enemy_width/2 - 30, self.y - 12))
            screen.blit(self.image, (self.x + self.enemy_width/2 - 12, self.y - 12))
            screen.blit(self.image, (self.x + self.enemy_width/2 + 6, self.y - 12))
