"""Module providing a function printing python version."""
import pygame
import sys
import random
import time
from os.path import join

pygame.init()
pygame.font.init()

#the screen
WIDTH = 800
LENGTH = 600
window = pygame.display.set_mode([WIDTH, LENGTH])
background = pygame.image.load("stars.jpg") # put stars image here
fps = 60
timer = pygame.time.Clock()

#imports image for player sprite and scales to smaller size
player_sprite = pygame.image.load(join("sprites","player0.png"))
player_sprite = pygame.transform.scale_by(player_sprite,(0.5,0.5))
player_sprite_height = player_sprite.get_height()
player_sprite_width = player_sprite.get_width()

#define colours for random rectangles
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
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
    
def show_start_screen():
    play_button = Button(WIDTH // 2 - 100, LENGTH // 2 - 25, 200, 50, GREEN, "Play")
    my_font = pygame.font.SysFont('Comic Sans MS', 80)
    while True:
        window.fill(RED)
        text_surface = my_font.render('Awesome Cross V2', False, (0, 0, 0))
        window.blit(text_surface, (55,150))
        play_button.draw(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(event.pos):
                    game_loop()  # Exit the start screen loop and start the game
        
        pygame.display.flip()
        timer.tick(fps)
        
def game_over_screen():
    replay_button = Button(WIDTH // 2 - 100, LENGTH // 2 - 25, 200, 50, GREEN, "Try again")
    my_font = pygame.font.SysFont('Comic Sans MS', 80)
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
                    game_loop()  # Exit the start screen loop and start the game
        
        pygame.display.flip()
        timer.tick(fps)
    

def game_loop():
    #character stuff
    character_radius = 30
    character_x = WIDTH // 2
    character_y = 450
    lives = 3;
    speed = 7
    obstacle_speed = 6
    grace_time = 3
    game_start_time = time.time()

    #for background start
    x = 0
    y = 0


    #Makes random rectangles to collide with
    obstacles=[]
    for _ in range(15):
        obstacle_rect = pygame.Rect(random.randint(0, 500), random.randint(-400, 0), 25, 25)
        obstacles.append(obstacle_rect)
    

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
                    obstacles.remove(obstacle)  # Optional: remove the obstacle to avoid repeated collision
            
        
        # Handle blinking
        if blinking:
            if current_time - last_blink_time < blink_duration:
                col = RED
            else:
                blinking = False
        
    
        pygame.draw.circle(window, col, (character_x,character_y), character_radius)
        
        #draws player sprite onto circle
        window.blit(player_sprite,(character_x - (player_sprite_width/2),
                                 character_y - (player_sprite_height/2)))
                
        # Check if lives are depleted
        if lives <= 0:
            game_over_screen()  # we can replace this with an end game screen or restart logic
            
            
        lives_text = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = lives_text.render('Lives: ' + str(lives), False, (0, 255, 0))
        window.blit(text_surface, (5,560))
        
     
        pygame.display.flip()
    
def main():
    while True:
        show_start_screen()
        game_loop()
        
        
if __name__ == "__main__":
    main()
            
    
  
            