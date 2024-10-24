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
background = pygame.image.load(join('Cycle_2/sprites',"space.png")) # put stars image here
fps = 60
timing = 1
timer = pygame.time.Clock()
obstacle_speed = 3
powerup_speed = 3
game_speed = 6
obstacle_interval = 600  # how fast obstacles spawn
powerup_interval = random.randint(12000, 15000)
#powerup_interval = 2000

death_sound = pygame.mixer.Sound(join("Cycle_2/audio","deathSound.wav"))
hit_sound = pygame.mixer.Sound(join('Cycle_2/audio',"hit.wav"))

#player_images = [pygame.transform.scale(pygame.image.load(join('Cycle_2/sprites',f'cheat{i}.png')).convert_alpha(), (80,80)) for i in range(1, 5)]

#define colours for random rectangles
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)



def game_loop():
    global game_speed, obstacle_speed, powerup_speed
    playerInst = Player(WIDTH, LENGTH)
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
    
    
    # for the background
    x = 0
    y = 0
    
    #random variable test
    z = 0
    
    #finishline, change both because total_distance is needed for progress bar
    finish_line_y = -30000
    total_distance = -30000
      
    game_finished = False
    stop_moving = False
    
    start_time = time.time()
    speedup_interval = 10  #every 10 seconds game gets faster
    
    running = True
    while running:
        timer.tick(fps)
        current_time = time.time()
        
        #for the game getting faster every set time
        if(current_time - start_time >= speedup_interval):
            game_speed += 0.6  #how fast the background moves
            obstacle_speed += 0.3 #obstacles --
            powerup_speed += 0.3  #powerups --  both of these need to be half the game speed to align
            playerInst.speed += 0.6  # player speed gets faster to compensate
            start_time = current_time  # loop

        
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
                powerup_spawned = False
                while not powerup_spawned:
                    # make powerup
                    new_powerup = Invincibility(powerup_speed, WIDTH, LENGTH)
                    
                    # check collision with obstacle
                    collided_obstacles = pygame.sprite.spritecollide(new_powerup, obstacle_group, dokill=False)
                    if collided_obstacles:
                        new_powerup.kill()
                    # If no collision, add the power-up to the groups and break the loop
                    if not collided_obstacles:
                        all_sprites.add(new_powerup)
                        powerup_group.add(new_powerup)
                        powerup_spawned = True  # Exit the loop after successful spawn
                    
        
        obstacle_group.update()
        powerup_group.update()
                    
        # #Movement
        playerInst.move()
                    
        # Scrolling background
        y += game_speed  # How fast it scrolls
        if finish_line_y < -5:
            finish_line_y += 6
        if finish_line_y > -500:
            game_finished = True
        if finish_line_y > -100:
            playerInst.stop_moving = True
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
                pygame.mixer.Sound.play(hit_sound)
                playerInst.lives -= 1
            
            
        collided_powerups = pygame.sprite.spritecollide(playerInst, powerup_group, dokill=False)
        for powerup in collided_powerups:
            powerup.kill()
            powerup_active = True
            powerup_start_time = pygame.time.get_ticks()
            
        if powerup_active:
            current_ticks = pygame.time.get_ticks()
            if current_ticks - powerup_start_time < powerup_duration:
                y += game_speed * 2  # Example effect: double speed
                
                invincible = True
                for obstacle in obstacle_group:
                    obstacle.speed = obstacle_speed * 2
                for powerup in powerup_group:
                    powerup.speed = powerup_speed * 2
            else:
                powerup_active = False
                invincible = False
                
                y += 6  # Reset speed to normal
                for obstacle in obstacle_group:
                    obstacle.speed = obstacle_speed 
                for powerup in powerup_group:
                    powerup.speed = powerup_speed 
            
    
        # Finish line
        finish_line = pygame.Rect(0, finish_line_y, 800, 25)
        
        if playerInst.rect.colliderect(finish_line):
            screens.you_win_screen(WIDTH, LENGTH, window, game_loop)
            
       
       
        # Check if lives ran out
        if playerInst.lives <= 0:
            pygame.mixer.Sound.play(death_sound)
            screens.game_over_screen(WIDTH, LENGTH, window, game_loop)
            
        # Display lives
        lives_text = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = lives_text.render('Lives: ' + str(playerInst.lives), False, (0, 255, 0))
        window.blit(text_surface, (5, 560)) 

        # Displays score/Distance traveled
        score_text = pygame.font.SysFont('Comic Sans MS', 20)
        score_surface = score_text.render('Score: ' + str(abs(total_distance) + finish_line_y), False, 'yellow')
        window.blit(score_surface, (WIDTH - 150,5))
        
        # Draw finish line
        pygame.draw.rect(window, BLUE, finish_line)
        
         # Calculate progress
        progress = 1 - (finish_line_y / total_distance)
        
        # Draw progress bar
        progress_bar_width = 200
        progress_bar_height = 20
        progress_bar_x = (WIDTH - progress_bar_width) // 2
        progress_bar_y = 10
        #draw white
        pygame.draw.rect(window, (255, 255, 255), (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height), 2)
        #draw green (moving)
        filled_width = int(progress * progress_bar_width)
        pygame.draw.rect(window, (0, 255, 0), (progress_bar_x, progress_bar_y, filled_width, progress_bar_height))
        
        
        pygame.display.flip()
        
def main():
    while True:
        screens.show_start_screen(WIDTH, LENGTH, window, game_loop)
        game_loop()
        
if __name__ == "__main__":
    main()