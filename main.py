"""Module providing a function printing python version."""
import pygame
import sys

pygame.init()

WIDTH = 800
LENGTH = 600
window = pygame.display.set_mode([WIDTH, LENGTH])
background = (0,0,0)
fps = 60
timer = pygame.time.Clock()
speed = 5
character_radius = 50
character_x = WIDTH // 2
character_y = LENGTH // 2

running = True
while running:
    timer.tick(fps)
    window.fill(background)
    character = pygame.draw.circle(window, [255,0,0], [character_x,character_y], 40, 0 )
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        character_y -= speed
    if keys[pygame.K_a]:
        character_x -= speed
    if keys[pygame.K_s]:
        character_y += speed
    if keys[pygame.K_d]:
        character_x += speed
        
    pygame.display.flip()
    

            
    
  
            