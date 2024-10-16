import pygame
import sys
import random
import time

class Player(pygame.sprite.Sprite):
    def __init__(self, WIDTH, LENGTH, player_images):
        super().__init__()
        self.images = player_images
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