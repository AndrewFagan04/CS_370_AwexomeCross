import pygame
import random
from os.path import join
#mostly same as Obstacle.py

class Invincibility(pygame.sprite.Sprite):
    def __init__(self, obstacle_speed, WIDTH, LENGTH):
        super().__init__()
        #self.image = pygame.image.load("C:/Users/Danyal/CS_370_danyalm/CS_370_AwexomeCross/Cycle/sprites/coin.png")
        self.image = pygame.image.load(join('Cycle\sprites',"coin.png"))

        self.image = pygame.transform.scale(self.image, (100, 100)) 
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width) 
        self.rect.y = -self.rect.height
        self.speed = obstacle_speed  
        self.LENGTH = LENGTH 

    def update(self):
        self.rect.y += self.speed  
        if self.rect.y > self.LENGTH:  
            self.kill()
