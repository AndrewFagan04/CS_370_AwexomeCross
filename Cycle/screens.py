import pygame
import sys
import random
import time

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
fps = 60

class Button:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surf = self.font.render(self.text, True, BLUE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def show_start_screen(WIDTH, LENGTH, window, game_loop):
    play_button = Button(WIDTH // 2 - 100, LENGTH // 2 - 25, 200, 50, GREEN, "Play")
    my_font = pygame.font.SysFont('Comic Sans MS', 80)
    
    while True:
        window.fill(RED)
        text_surface = my_font.render('Awesome Cross V2', False, (0, 0, 0))
        window.blit(text_surface, (55, 150))
        play_button.draw(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(event.pos):
                    game_loop() 
        
        pygame.display.flip()
        pygame.time.Clock().tick(fps)
 
      
def game_over_screen(WIDTH, LENGTH, window, game_loop):
    replay_button = Button(WIDTH // 2 - 100, LENGTH // 2 - 25, 200, 50, GREEN, "Try again")
    my_font = pygame.font.SysFont('Comic Sans MS', 60)
    while True:
        window.fill(RED)
        text_surface = my_font.render('Game Over!', False, (0, 0, 0))
        window.blit(text_surface, (190,150))
        replay_button.draw(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.is_clicked(event.pos):
                    game_loop() 
        
        pygame.display.flip()
        pygame.time.Clock().tick(fps)
        
def you_win_screen(WIDTH, LENGTH, window, game_loop):
    play_button = Button(WIDTH // 2 - 100, LENGTH // 2 - 25, 200, 50, GREEN, "Play Again")
    my_font = pygame.font.SysFont('Comic Sans MS', 60)
    while True:
        window.fill(RED)
        text_surface = my_font.render('You Win!', False, (0, 0, 0))
        window.blit(text_surface, (240,150))
        play_button.draw(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(event.pos):
                    game_loop()
        
        pygame.display.flip()
        pygame.time.Clock().tick(fps)

