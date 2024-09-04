import pygame
import sys
import random

pygame.init()

#Setting the window name, size, and color
WIDTH = 800
LENGTH = 600
pygame.display.set_caption("Collision w/ wasd")
window = pygame.display.set_mode([WIDTH, LENGTH])
background = (0,0,0)


#
fps = 60
timer = pygame.time.Clock()
speed = 5
character_x = WIDTH // 2
character_y = LENGTH // 2

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
    window.fill(background)
    character = pygame.Rect(0, 0, 25, 25)

    #check collision and change colour
    col = GREEN
    for obstacle in obstacles:
        if character.colliderect(obstacle):
            col = RED

    #draw all rectangles  
    pygame.draw.rect(window, col, character)
    for obstacle in obstacles:
        pygame.draw.rect(window, BLUE, obstacle)


    #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #Controlling character with wasd
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

pygame.quit()