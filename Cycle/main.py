import pygame
import sys
import random
import time
from player import Player
from obstacle import Obstacle
from powerups import Invincibility
import screens
from os.path import join
pygame.init()
pygame.font.init()

#the screen
WIDTH = 600
LENGTH = 600
window = pygame.display.set_mode([WIDTH, LENGTH])
background = pygame.image.load("space.png") # put stars image here
fps = 60
timing = 1
timer = pygame.time.Clock()
obstacle_speed = 3
obstacle_interval = 600  # how fast obstacles spawn
powerup_interval = 2000

player_images = [pygame.transform.scale(pygame.image.load(join('sprites',f'player{i}.png')).convert_alpha(), (28,103)) for i in range(1, 5)]

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
    powerup_group = pygame.sprite.Group()
    
    obstacle_event = pygame.USEREVENT + 1
    powerup_event = pygame.USEREVENT + 2

    pygame.time.set_timer(obstacle_event, obstacle_interval)
    pygame.time.set_timer(powerup_event, powerup_interval)
    
    # Power-up state tracking
    powerup_active = False
    powerup_start = 0
    powerup_duration = 2000  # 5 seconds for power-up effect
    invincible = False
    

    #character settings   
    lives = 3
    speed = 7
    
    # for the background
    x = 0
    y = 0
    
    #random variable test
    z = 0
    
    #finishline
    finish_line_y = -5000
    total_distance = -5000
      
    game_finished = False
    stop_moving = False
    
    running = True
    while running:
        timer.tick(fps)
        current_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == obstacle_event and not game_finished:
                #creating obstacle
                new_obstacle = Obstacle(obstacle_speed, WIDTH, LENGTH)
                all_sprites.add(new_obstacle)  
                obstacle_group.add(new_obstacle)
            elif event.type == powerup_event and not game_finished:
                #create invincibility powerup
                new_powerup = Invincibility(obstacle_speed, WIDTH, LENGTH)
                all_sprites.add(new_powerup)
                powerup_group.add(new_powerup)
        
        obstacle_group.update()
        powerup_group.update()
                    
        #Movement
        keys = pygame.key.get_pressed()
        #condition for when player gets near finish line
        if stop_moving == False:
            if keys[pygame.K_w]:
                playerInst.rect.y -= speed
            if keys[pygame.K_s]:
                playerInst.rect.y += speed
        
        if keys[pygame.K_a]:
                playerInst.rect.x -= speed
        if keys[pygame.K_d]:
                playerInst.rect.x += speed
            
        #Borders
        playerInst.rect.x = max(0, min(WIDTH - playerInst.rect.width, playerInst.rect.x))
        playerInst.rect.y = max(0, min(LENGTH - playerInst.rect.height, playerInst.rect.y))
                    
        # Scrolling background
        y += 6  # How fast it scrolls
        if finish_line_y < -5:
            finish_line_y += 6
        if finish_line_y > -500:
            game_finished = True
        if finish_line_y > -100:
            stop_moving = True
            playerInst.rect.y -= 5
            
        if y >= LENGTH:
            y = 0
        window.blit(background, (x, y))
        window.blit(background, (x, y - LENGTH))
        
        # draw sprites
        all_sprites.update()
        obstacle_group.draw(window)
        powerup_group.draw(window)
        window.blit(playerInst.image, playerInst.rect)

        
        if invincible == False:
            # player/obstacle COLLISION
            collided_obstacles = pygame.sprite.spritecollide(playerInst, obstacle_group, dokill=False)
            for obstacle in collided_obstacles:
                obstacle.kill()  # remove obstacle after hitting it
                lives -= 1
            
            
        collided_powerups = pygame.sprite.spritecollide(playerInst, powerup_group, dokill=False)
        for powerup in collided_powerups:
            powerup.kill()
            powerup_active = True
            powerup_start_time = pygame.time.get_ticks()
            
        if powerup_active:
            current_ticks = pygame.time.get_ticks()
            if current_ticks - powerup_start_time < powerup_duration:
                y += 10  # Example effect: double speed
                invincible = True
            else:
                powerup_active = False
                invincible = False
                y += 6  # Reset speed to normal
            
        
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
        
         # Calculate progress
        distance_covered = abs(playerInst.rect.y)
        progress = 1- (finish_line_y / total_distance)
        print(progress)
        
        # Draw progress bar
        progress_bar_width = 200
        progress_bar_height = 20
        progress_bar_x = (WIDTH - progress_bar_width) // 2
        progress_bar_y = 10
        pygame.draw.rect(window, (255, 255, 255), (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height), 2)
        filled_width = int(progress * progress_bar_width)
        pygame.draw.rect(window, (0, 255, 0), (progress_bar_x, progress_bar_y, filled_width, progress_bar_height))
        
        
        pygame.display.flip()
        
def main():
    while True:
        screens.show_start_screen(WIDTH, LENGTH, window, game_loop)
        game_loop()
        
if __name__ == "__main__":
    main()