import pygame
import sys
import random
import time
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, WIDTH, LENGTH):
        super().__init__()

        # Player flags
        self.stop_moving = False

        # Player Attributes
        self.speed = 7
        self.lives = 3
        
        # Window Width + Height
        self.winWIDTH = WIDTH
        self.winLENGTH = LENGTH

        # Load Player Sprite Images
        self.images = [pygame.transform.scale
                         (pygame.image.load(
                             join('Cycle_2/sprites',f'cheat{i}.png')).convert_alpha(), (80,80)) 
                                for i in range(1, 5)]
        # Animation
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, LENGTH - 100)
        self.animation_speed = 0.1
        self.last_update = pygame.time.get_ticks()


    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]
            self.last_update = now

    def move(self):
        keys = pygame.key.get_pressed()

        # Condition for when player gets near finish line
        if self.stop_moving == False:
            if keys[pygame.K_w]:
                self.rect.y -= self.speed
            if keys[pygame.K_s]:
                self.rect.y += self.speed
            
        if keys[pygame.K_a]:
                self.rect.x -= self.speed
        if keys[pygame.K_d]:
                self.rect.x += self.speed

        # Borders for player
        self.rect.x = max(0, min(self.winWIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(self.winLENGTH - self.rect.height, self.rect.y))