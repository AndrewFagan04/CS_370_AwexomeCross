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
background = pygame.image.load("C:/Users/Danyal/CS_370_danyalm/CS_370_AwexomeCross/spacee.jpg") # put stars image here
meteor = pygame.image.load("C:/Users/Danyal/CS_370_danyalm/CS_370_AwexomeCross/sprites/Meteor_01.png")
fps = 60
timer = pygame.time.Clock()

#define colours for random rectangles
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

player_images = [pygame.transform.scale(pygame.image.load(f'C:/Users/Danyal/CS_370_danyalm/CS_370_AwexomeCross/sprites/player{i}.png').convert_alpha(), (28,103)) for i in range(1, 5)]
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
    lives = 3
    speed = 7
    obstacle_speed = 6
    grace_time = 3
    game_start_time = time.time()

    #for background start
    x = 0
    y = 0
     # Load meteor image
    meteor_img = pygame.transform.scale(meteor, (100, 100))  
    meteor_rect = meteor_img.get_rect()


    #Makes random meteors to collide with
    obstacles=[]
    for _ in range(5):
        obstacle_rect = meteor_rect.copy()
        obstacle_rect.x = random.randint(0, WIDTH - obstacle_rect.width)
        obstacle_rect.y = random.randint(-700, -300)
        obstacles.append((obstacle_rect, meteor_img))
    

    # Blink parameters
    last_blink_time = 0
    blinking = False
    blink_duration = 0.15
    finish_line_y = -20000 #change this to make the game longer or shorter (smaller number is longer game)
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
        
        finish_line = pygame.Rect(0, finish_line_y, 800, 25)
        #scrolling background
        y += 6 #how fast it scrolls
        finish_line_y += 6
        if y == LENGTH:
            y = 0
        window.blit(background, (x, y))
        window.blit(background, (x, y - LENGTH))    
        
        #move obstacles
        for i, (obstacle_rect, _) in enumerate(obstacles):
            obstacle_rect.y += obstacle_speed
            if obstacle_rect.y > LENGTH:
                # Respawn meteor off-screen above
                obstacle_rect.y = random.randint(-obstacle_rect.height, -1 * meteor_rect.height)
                obstacle_rect.x = random.randint(0, WIDTH - obstacle_rect.width)
                    
        # Draw all meteors  
        for obstacle_rect, obstacle_img in obstacles:
            window.blit(obstacle_img, obstacle_rect.topleft)
            
        # Update and draw all sprites
        all_sprites.update()
        all_sprites.draw(window)
                    
            
        #check collision and change colour
        col = GREEN
        for obstacle_rect, _ in obstacles:
            if player.rect.colliderect(obstacle_rect):
                if not blinking:
                    blinking = True
                    last_blink_time = current_time
                    col = RED
                    lives -= 1  # Deduct a life on collision
                    obstacles.remove((obstacle_rect, _))  # Remove the obstacle to avoid repeated collision
                    
        
        if player.rect.colliderect(finish_line):
            show_start_screen()
                    
            
            
        
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
        
        pygame.draw.rect(window, BLUE, finish_line)
        
     
        pygame.display.flip()
    
def main():
    while True:
        show_start_screen()
        game_loop()
        
        
if __name__ == "__main__":
    main()
            
    
  
            