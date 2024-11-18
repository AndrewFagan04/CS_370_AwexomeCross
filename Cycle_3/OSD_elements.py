import pygame
import sys
import random
import time
from os.path import join
from player import Player

class lives:
    def update_lives(playerInst,window):
        lives_text = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = lives_text.render('Lives: ' + str(playerInst.lives), False, (0, 255, 0))
        window.blit(text_surface, (5, 560)) 

class progress_bar:
    def __init__(self,WIDTH):
        # Draw self.progress bar
        self.progress_bar_width = 200
        self.progress_bar_height = 20
        self.progress_bar_x = (WIDTH - self.progress_bar_width) // 2
        self.progress_bar_y = 10

    def update_progress_bar(self,progress,window):
        #draw white
        pygame.draw.rect(window, (255, 255, 255), (self.progress_bar_x, self.progress_bar_y, self.progress_bar_width, self.progress_bar_height), 2)
        #draw green (moving)
        filled_width = int(progress * self.progress_bar_width)
        pygame.draw.rect(window, (0, 255, 0), (self.progress_bar_x, self.progress_bar_y, filled_width, self.progress_bar_height))

class score:
    def display_score(playerInst,window,WIDTH):
        score_text = pygame.font.SysFont('Comic Sans MS', 20)
        score_surface = score_text.render('Score: ' + str(int(playerInst.score)), False, 'yellow')
        window.blit(score_surface, (WIDTH - 150,5))
