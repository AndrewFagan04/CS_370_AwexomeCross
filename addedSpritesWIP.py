"""Module providing a function printing python version."""
import pygame
import sys
import random
import time

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("spaceMusic.wav")
pygame.mixer.music.play(-1,0.0)

#the screen
WIDTH = 800
LENGTH = 600
window = pygame.display.set_mode([WIDTH, LENGTH])
background = pygame.image.load("spacee.jpg") # put stars image here
fps = 60
timer = pygame.time.Clock()


#character stuff
character_radius = 30
character_x = WIDTH // 2
character_y = 450
lives = 3
speed = 7
obstacle_speed = 6
grace_time = 3
game_start_time = time.time()

#for background start
x = 0
y = 0

#getting hit sound effect
hit_sfx = pygame.mixer.Sound("hit.wav")
thruster_sfx = pygame.mixer.Sound("thrusters.wav")
death_sfx = pygame.mixer.Sound("deathSound.wav")

#Makes random rectangles to collide with
obstacles=[]
for _ in range(15):
    obstacle_rect = pygame.Rect(random.randint(0, 500), random.randint(-400, 0), 25, 25)
    obstacles.append(obstacle_rect)
  
  #define colours for random rectangles
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Blink parameters
last_blink_time = 0
blinking = False
blink_duration = 0.15

running = True
#--------------------------------------------
while running:
    timer.tick(fps)
    current_time = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    #moving side to side
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        character_y -= speed
        pygame.mixer.Channel.play()
        pygame.mixer.Channel.stop()
    if keys[pygame.K_a]:
        character_x -= speed
    if keys[pygame.K_s]:
        character_y += speed
    if keys[pygame.K_d]:
        character_x += speed
        
    #borders so character doesn't move out of the screen   
    character_x = max(character_radius, min(WIDTH - character_radius, character_x))
    character_y = max(character_radius, min(LENGTH - character_radius, character_y))
    
            
    #scrolling background
    y += 6 #how fast it scrolls
    if y == LENGTH:
        y = 0
    window.blit(background, (x, y))
    window.blit(background, (x, y - LENGTH))    
        #move rectangles
    for obstacle in obstacles:
        obstacle.y += obstacle_speed
        if obstacle.y > LENGTH:
            obstacle.y = -obstacle_speed  # Respawn at the top
            obstacle.x = random.randint(0, WIDTH - obstacle_speed)  # Random new horizontal position
        
                
    #draw all rectangles  
    for obstacle in obstacles:
        pygame.draw.rect(window, BLUE, obstacle)
                   
        
    #check collision and change colour
    character = pygame.Rect(character_x - character_radius, character_y - character_radius, character_radius * 2, character_radius * 2)
    col = GREEN
    for obstacle in obstacles:
        if character.colliderect(obstacle):
            if not blinking:
                blinking = True
                last_blink_time = current_time
                col = RED
                lives -= 1  # Deduct a life on collision
                hit_sfx.play() #plays hit sound when hit
                obstacles.remove(obstacle)  # Optional: remove the obstacle to avoid repeated collision
        
     
    # Handle blinking
    if blinking:
        if current_time - last_blink_time < blink_duration:
            col = RED
        else:
            blinking = False
      
      
    pygame.draw.circle(window, col, (character_x,character_y), character_radius)
             
    # Check if lives are depleted
    if lives <= 0:
        death_sfx.play()
        pygame.time.wait(2000)
        print("Game Over!")  # we can replace this with an end game screen or restart logic
        running = False
        
        
        
        
    pygame.display.flip()
    

            
    
  
            