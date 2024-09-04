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


#character circle and speed
character_radius = 30
character_x = WIDTH // 2
character_y = 450
speed = 10

running = True
while running:
    timer.tick(fps)
    window.fill(background)
    
    #character circle (change to sprite later)
    character = pygame.draw.circle(window, [255,0,0], [character_x,character_y], character_radius, 0 )
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    #moving side to side
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        character_x -= speed
    if keys[pygame.K_d]:
        character_x += speed
        
    #borders so character doesn't move out of the screen   
    if character_x < WIDTH - WIDTH + character_radius:
        character_x = WIDTH - WIDTH + character_radius
    if character_x > WIDTH - character_radius:
        character_x = WIDTH - character_radius
        
        
    pygame.display.flip()
    

            
    
  
            