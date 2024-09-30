import pygame
import random
from os.path import join

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_speed, WIDTH, LENGTH):
        super().__init__()
        self.image = pygame.image.load(join('sprites',"Meteor_06.png"))
        self.image = pygame.transform.scale(self.image, (100, 100))  # Ensure the image is scaled to 100x100

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)  # Ensure valid range
        self.rect.y = -self.rect.height
        self.speed = obstacle_speed  # Store the speed
        self.LENGTH = LENGTH  # Store the length of the game window

    def update(self):
        self.rect.y += self.speed  # Use the stored speed
        if self.rect.y > self.LENGTH:  # Use the stored length
            self.kill()
