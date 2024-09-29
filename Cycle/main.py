import pygame
import sys
import random
import time
from player import Player
from obstacle import Obstacle
import screens

pygame.init()
pygame.font.init()

#the screen
WIDTH = 600
LENGTH = 600
window = pygame.display.set_mode([WIDTH, LENGTH])
background = pygame.image.load("stars.jpg") # put stars image here
fps = 60
timer = pygame.time.Clock()
obstacle_speed = 3
obstacle_interval = 600  # how fast obstacles spawn

player_images = [pygame.transform.scale(pygame.image.load(f'C:/Users/Danyal/CS_370_danyalm/CS_370_AwexomeCross/Cycle/sprites/player{i}.png').convert_alpha(), (28,103)) for i in range(1, 5)]

#define colours for random rectangles
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)


def game_loop():
    playerInst = Player(WIDTH, LENGTH, player_images)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(playerInst)
    
    obstacle_group = pygame.sprite.Group()
    pygame.time.set_timer(pygame.USEREVENT, obstacle_interval)
    

    #character settings   
    lives = 3
    speed = 7
    
    # for the background
    x = 0
    y = 0
    
    #finishline
    finish_line_y = -1000
      
    running = True
    while running:
        timer.tick(fps)
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT:
                new_obstacle = Obstacle(obstacle_speed, WIDTH, LENGTH)
                all_sprites.add(new_obstacle)  
                obstacle_group.add(new_obstacle)
                
        obstacle_group.update()
                    
        #Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            playerInst.rect.y -= speed
        if keys[pygame.K_a]:
            playerInst.rect.x -= speed
        if keys[pygame.K_s]:
            playerInst.rect.y += speed
        if keys[pygame.K_d]:
            playerInst.rect.x += speed
            
        #Borders
        playerInst.rect.x = max(0, min(WIDTH - playerInst.rect.width, playerInst.rect.x))
        playerInst.rect.y = max(0, min(LENGTH - playerInst.rect.height, playerInst.rect.y))
                    
        # Scrolling background
        y += 6  # How fast it scrolls
        finish_line_y += 6
        if finish_line_y > LENGTH:
            finish_line_y = LENGTH
        if y >= LENGTH:
            y = 0
        window.blit(background, (x, y))
        window.blit(background, (x, y - LENGTH))
        print(finish_line_y)
        
        # draw sprites
        all_sprites.update()
        all_sprites.draw(window)
        
        # player/obstacle COLLISION
        collided_obstacles = pygame.sprite.spritecollide(playerInst, obstacle_group, dokill=False)
        for obstacle in collided_obstacles:
            obstacle.kill()  # remove obstacle after hitting it
            lives -= 1
            
        # Finish line
        finish_line = pygame.Rect(0, finish_line_y, 800, 25)
        
        if playerInst.rect.colliderect(finish_line):
            screens.you_win_screen(WIDTH, LENGTH, window, game_loop)
            
       
       
        # Check if lives ran out
        if lives <= 0:
            screens.game_over_screen(WIDTH, LENGTH, window, game_loop)
            
        # Display lives
        lives_text = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = lives_text.render('Lives: ' + str(lives), False, (0, 255, 0))
        window.blit(text_surface, (5, 560)) 
        
        # Draw finish line
        pygame.draw.rect(window, BLUE, finish_line)
        
        pygame.display.flip()
        
def main():
    while True:
        screens.show_start_screen(WIDTH, LENGTH, window, game_loop)
        game_loop()
        
if __name__ == "__main__":
    main()