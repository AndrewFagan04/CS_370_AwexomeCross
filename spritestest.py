"""Module providing a function printing python version."""
import pygame
import sys
import random
import time

pygame.init()
pygame.font.init()

#the screen
WIDTH = 800
LENGTH = 600
window = pygame.display.set_mode([WIDTH, LENGTH])
background = pygame.image.load("spacee.jpg") # put stars image here
fps = 60
timer = pygame.time.Clock()

#define colours for random rectangles
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

player_images = [pygame.transform.scale(pygame.image.load(f'sprites/player{i}.png').convert_alpha(), (28,103)) for i in range(1, 5)]
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = player_images
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, LENGTH - 100)
        self.animation_speed = 0.1
        self.last_update = time.time()

    def update(self):
        now = time.time()
        if now - self.last_update > self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]
            self.last_update = now

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
    
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    
    #character stuff
    character_radius = 30
    character_x = WIDTH // 2
    character_y = 450
    lives = 3;
    speed = 4
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
            player.rect.y -= speed
        if keys[pygame.K_a]:
            player.rect.x -= speed
        if keys[pygame.K_s]:
            player.rect.y += speed
        if keys[pygame.K_d]:
            player.rect.x += speed
            
        #borders so character doesn't move out of the screen   
        player.rect.x = max(0, min(WIDTH - player.rect.width, player.rect.x))
        player.rect.y = max(0, min(LENGTH - player.rect.height, player.rect.y))
        
                
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
            
        # Update and draw all sprites
        all_sprites.update()
        all_sprites.draw(window)
                    
            
        #check collision and change colour
        col = GREEN
        for obstacle in obstacles:
            if player.rect.colliderect(obstacle):
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
            
    
  
            