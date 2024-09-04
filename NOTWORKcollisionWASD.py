"""Module providing a function printing python version."""
import pygame
import sys
import random

pygame.init()

WIDTH = 800
LENGTH = 600

window = pygame.display.set_mode([WIDTH, LENGTH])
background = pygame.image.load("spacee.jpg") # put stars image here

fps = 60
timer = pygame.time.Clock()


#character circle and speed
character_radius = 30
character_x = WIDTH // 2
character_y = 450
speed = 10

#for background start
x = 0
y = 0

#Makes random rectangles to collide with
obstacles = []
for _ in range(16):
  obstacle_rect = pygame.Rect(random.randint(0, 500), random.randint(0, 300), 25, 25)
  obstacles.append(obstacle_rect)
  
  #define colours for random rectangles
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

running = True
while running:
    timer.tick(fps)
    
    #scrolling background
    
    #y += 3 #how fast it scrolls
    
    #if y == LENGTH:
    #    y = 0
    window.blit(background, (x, y))
    #window.blit(background, (x, y - LENGTH))
    
    #character circle (change to sprite later)
    character = pygame.draw.circle(window, [255,0,0], [character_x,character_y], character_radius, 0 )
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    #moving side to side
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        character_y -= speed
    if keys[pygame.K_a]:
        character_x -= speed
    if keys[pygame.K_s]:
        character_y += speed
    if keys[pygame.K_d]:
        character_x += speed
        
    #borders so character doesn't move out of the screen   
    if character_x < WIDTH - WIDTH + character_radius:
        character_x = WIDTH - WIDTH + character_radius
    if character_x > WIDTH - character_radius:
        character_x = WIDTH - character_radius
        
    #check collision and change colour
    col = GREEN
    for obstacle in obstacles:
        if character.colliderect(obstacle):
            col = RED
        
    #draw all rectangles  
    pygame.draw.rect(window, col, character)
    for obstacle in obstacles:
        pygame.draw.rect(window, BLUE, obstacle)
        
        
    pygame.display.flip()
    

            
    
  
            