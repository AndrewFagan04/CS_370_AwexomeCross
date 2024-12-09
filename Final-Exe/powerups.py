import pygame
import random
from os.path import join
#mostly same as Obstacle.py

class Invincibility(pygame.sprite.Sprite):
    def __init__(self, powerup_speed, WIDTH, LENGTH):
        super().__init__()
        self.image = pygame.image.load(join('_internal/sprites',"gas_can2.png"))
        self.image = self.image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width) 
        self.rect.y = -self.rect.height
        self.speed = powerup_speed  
        self.LENGTH = LENGTH 

    def update(self):
        self.rect.y += self.speed  
        if self.rect.y > self.LENGTH:  
            self.kill()
            
class ExtraLives(pygame.sprite.Sprite):
    def __init__(self, powerup_speed, WIDTH, LENGTH):
        super().__init__()
        self.image = pygame.image.load(join('_internal/sprites',"heart.png"))
        self.image = self.image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (130, 100))

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width) 
        self.rect.y = -self.rect.height
        self.speed = powerup_speed  
        self.LENGTH = LENGTH 

    def update(self):
        self.rect.y += self.speed  
        if self.rect.y > self.LENGTH:  
            self.kill()
