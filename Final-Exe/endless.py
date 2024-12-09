import pygame
import sys
import random
import time
from player import Player
from obstacle import Obstacle
from powerups import Invincibility
from powerups import ExtraLives
from OSD_elements import *
import screens
from os.path import join
import cv2
pygame.init()
pygame.font.init()
#the screen
WIDTH = 600
LENGTH = 600
window = pygame.display.set_mode([WIDTH, LENGTH])
background = pygame.image.load(join('_internal/sprites',"space.png")) # put stars image here
fps = 60
timing = 1
timer = pygame.time.Clock()
obstacle_speed = 3
powerup_speed = 3
game_speed = 6
obstacle_interval = 600  # how fast obstacles spawn
invincible_interval = random.randint(11000, 15000)
extra_interval = random.randint(18000, 22000)
high_scores = []



death_sound = pygame.mixer.Sound(join("_internal/audio","deathSound.wav"))
hit_sound = pygame.mixer.Sound(join('_internal/audio',"hit.wav"))

#define colours for random rectangles
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)


def game_loop_endless():
    global game_speed, obstacle_speed, powerup_speed
    playerInst = Player(WIDTH, LENGTH)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(playerInst)
    
    obstacle_group = pygame.sprite.Group()
    invincible_group = pygame.sprite.Group()
    extra_group = pygame.sprite.Group()
    
    obstacle_event = pygame.USEREVENT + 1
    invincible_event = pygame.USEREVENT + 2
    extra_event = pygame.USEREVENT + 3

    pygame.time.set_timer(obstacle_event, obstacle_interval)
    pygame.time.set_timer(invincible_event, invincible_interval)
    pygame.time.set_timer(extra_event, extra_interval)
    
    # Power-up state tracking
    invincible_active = False
    invincible_start = 0
    invincible_duration = 2000  # 5 seconds for power-up effect
    invincible = False
    
    # for the background
    x = 0
    y = 0
    
    #random variable test
    z = 0
    
    # Remove finish_line and total_distance for endless mode
    finish_line_y = -30000
    total_distance = 100000  # You can set it as large as you want to simulate distance.
      
    game_finished = False
    stop_moving = False
    
    start_time = time.time()
    speedup_interval = 10  # Every 10 seconds game gets faster

   
    
    running = True
    while running:
        timer.tick(fps)
        current_time = time.time()
        
        # Game speed increase over time
        if(current_time - start_time >= speedup_interval):
            game_speed += 0.6  # Speed of the background scroll
            obstacle_speed += 0.3 # Speed of obstacles
            powerup_speed += 0.3  # Speed of powerups
            playerInst.speed += 0.6  # Speed of the player
            start_time = current_time  # Loop the speed increase
            for obstacle in obstacle_group:
                obstacle.speed = obstacle_speed
            for powerup in invincible_group:
                powerup.speed = powerup_speed
            for powerup in extra_group:
                powerup.speed = powerup_speed

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == obstacle_event and not game_finished:
                # Creating obstacle
                new_obstacle = Obstacle(obstacle_speed, WIDTH, LENGTH)
                all_sprites.add(new_obstacle)  
                obstacle_group.add(new_obstacle)
            elif event.type == extra_event and not game_finished:
                powerup_spawned = False
                while not powerup_spawned:
                    # Make powerup
                    new_extra = ExtraLives(powerup_speed, WIDTH, LENGTH)
                    
                    # Check collision with obstacle
                    collided_obstacles = pygame.sprite.spritecollide(new_extra, obstacle_group, dokill=False)
                    if collided_obstacles:
                        new_extra.kill()
                    # If no collision, add the power-up to the groups and break the loop
                    if not collided_obstacles:
                        all_sprites.add(new_extra)
                        extra_group.add(new_extra)
                        powerup_spawned = True  # Exit the loop after successful spawn
            elif event.type == invincible_event and not game_finished:
                powerup_spawned = False
                while not powerup_spawned:
                    # Make powerup
                    new_invincible = Invincibility(powerup_speed, WIDTH, LENGTH)
                    
                    # Check collision with obstacle
                    collided_obstacles = pygame.sprite.spritecollide(new_invincible, obstacle_group, dokill=False)
                    if collided_obstacles:
                        new_invincible.kill()
                    # If no collision, add the power-up to the groups and break the loop
                    if not collided_obstacles:
                        all_sprites.add(new_invincible)
                        invincible_group.add(new_invincible)
                        powerup_spawned = True  # Exit the loop after successful spawn
        
        obstacle_group.update()
        invincible_group.update()
        extra_group.update()
                    
        # Movement
        playerInst.move()
                    
        # Scrolling background
        y += game_speed  # How fast it scrolls
        
        if y >= LENGTH:
            y = 0
        window.blit(background, (x, y))
        window.blit(background, (x, y - LENGTH))
        
        # Draw sprites
        all_sprites.update()
        obstacle_group.draw(window)
        invincible_group.draw(window)
        extra_group.draw(window)
        window.blit(playerInst.image, playerInst.rect)

        
        if invincible == False:
            # player/obstacle COLLISION
            collided_obstacles = pygame.sprite.spritecollide(playerInst, obstacle_group, dokill=False)
            for obstacle in collided_obstacles:
                obstacle.kill()  # remove obstacle after hitting it
                pygame.mixer.Sound.play(hit_sound)
                playerInst.lives -= 1
                
        collided_extra = pygame.sprite.spritecollide(playerInst, extra_group, dokill=False)
        for powerup in collided_extra:
            powerup.kill()
            playerInst.lives += 1
            playerInst.score += 5000 # gets extra points for collecting powerup
            

        collided_powerups = pygame.sprite.spritecollide(playerInst, invincible_group, dokill=False)
        for powerup in collided_powerups:
            powerup.kill()
            invincible_active = True
            invincible_start_time = pygame.time.get_ticks()
            playerInst.score += 5000 # gets extra points for collecting powerup
            
        if invincible_active:
            current_ticks = pygame.time.get_ticks()
            if current_ticks - invincible_start_time < invincible_duration:
                y += game_speed * 1.3  # Example effect: double speed
                invincible = True
                for obstacle in obstacle_group:
                    obstacle.speed = obstacle_speed * 2
                for powerup in invincible_group:
                    powerup.speed = powerup_speed * 2
                for powerup in extra_group:
                    powerup.speed = powerup_speed * 2
            else:
                invincible_active = False
                invincible = False
                
                y += 6  # Reset speed to normal
                for obstacle in obstacle_group:
                    obstacle.speed = obstacle_speed 
                for powerup in invincible_group:
                    powerup.speed = powerup_speed 
                for powerup in extra_group:
                    powerup.speed = powerup_speed 
            
    
        # Update score and distance traveled
        score.display_score(playerInst, window, WIDTH)
        
        # Check if lives ran out
        if playerInst.lives <= 0:
            pygame.mixer.Sound.play(death_sound)
            screens.add_high_score(high_scores, playerInst.score)
            screens.game_over_screen(WIDTH, LENGTH, window, game_loop_endless)
            
        # Display lives
        lives.update_lives(playerInst, window)

        # Updates score as long as player is alive
        if playerInst.stop_moving == False:
            playerInst.score += game_speed

        # Draw finish line (even though it's not used for end condition anymore)
        pygame.draw.rect(window, BLUE, pygame.Rect(0, finish_line_y, 800, 25))
        
        # Calculate progress
        progress = 1 - (finish_line_y / total_distance)

     
        
        pygame.display.flip()
        
def main():
    while True:
     
        game_loop_endless()
        
if __name__ == "__main__":
    main()