import pygame
import random

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_speed, WIDTH, LENGTH):
        super().__init__()
        self.image = pygame.image.load("C:/Users/Danyal/CS_370_danyalm/CS_370_AwexomeCross/sprites/Meteor_06.png")
        self.image = pygame.transform.scale(self.image, (100, 100))  #change how big it is
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width) #spawn in range
        self.rect.y = -self.rect.height
        self.speed = obstacle_speed  # speed
        self.LENGTH = LENGTH  # game window length, so i can use in the bottom function

    def update(self):
        #makes it move down at the speed
        self.rect.y += self.speed  
        if self.rect.y > self.LENGTH:
            self.kill()
