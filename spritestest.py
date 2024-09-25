import pygame
import sys
import random
import time
from os.path import join # join("filepath from working directory","filename") to get file instead of copying whole path

pygame.init()
pygame.font.init()

#the screen
WIDTH = 600
LENGTH = 600
window = pygame.display.set_mode([WIDTH, LENGTH])
background = pygame.image.load(join("space.png")) # put stars image here
fps = 60
timer = pygame.time.Clock()
obstacle_speed = 3
obstacle_interval = 600  # how fast obstacles spawn

#define colours for random rectangles
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)

player_images = [pygame.transform.scale(pygame.image.load(join('sprites',f'player{i}.png')).convert_alpha(), (28,103)) for i in range(1, 5)]
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = player_images
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, LENGTH - 100)
        self.animation_speed = 0.1
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
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
    
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(join('sprites',"Meteor_06.png"))
        self.image = pygame.transform.scale(self.image, (100, 100))  

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
    
    def update(self):
        self.rect.y += obstacle_speed
        if self.rect.y > LENGTH:
            self.kill()

obstacle_group = pygame.sprite.Group()
pygame.time.set_timer(pygame.USEREVENT, obstacle_interval)


    
def show_start_screen():
    play_button = Button(WIDTH // 2 - 100, LENGTH // 2 - 25, 200, 50, GREEN, "Play")
    my_font = pygame.font.SysFont('Comic Sans MS', 60)
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
                    game_loop() 
        
        pygame.display.flip()
        timer.tick(fps)
        
def game_over_screen():
    replay_button = Button(WIDTH // 2 - 100, LENGTH // 2 - 25, 200, 50, GREEN, "Try again")
    my_font = pygame.font.SysFont('Comic Sans MS', 60)
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
                    game_loop() 
        
        pygame.display.flip()
        timer.tick(fps)
    
def you_win_screen():
    play_button = Button(WIDTH // 2 - 100, LENGTH // 2 - 25, 200, 50, GREEN, "Play Again")
    my_font = pygame.font.SysFont('Comic Sans MS', 60)
    while True:
        window.fill(RED)
        text_surface = my_font.render('You Win!', False, (0, 0, 0))
        window.blit(text_surface, (240,150))
        play_button.draw(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(event.pos):
                    game_loop()
        
        pygame.display.flip()
        timer.tick(fps)
        


def game_loop():
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    
    obstacle_group = pygame.sprite.Group() 
    pygame.time.set_timer(pygame.USEREVENT, obstacle_interval)
    
    # Character settings
    lives = 3
    speed = 7
    collision_occured = False
    
    # for the background
    x = 0
    y = 0
      
    
    finish_line_y = -7000  # how long the game is (smaller number = longer game)
    running = True
    
    while running:
        timer.tick(fps)
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT:
                new_obstacle = Obstacle()
                all_sprites.add(new_obstacle)  
                obstacle_group.add(new_obstacle)
        
        obstacle_group.update()
        
        # Moving side to side
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.rect.y -= speed
        if keys[pygame.K_a]:
            player.rect.x -= speed
        if keys[pygame.K_s]:
            player.rect.y += speed
        if keys[pygame.K_d]:
            player.rect.x += speed
            
        # Borders so character doesn't move out of the screen
        player.rect.x = max(0, min(WIDTH - player.rect.width, player.rect.x))
        player.rect.y = max(0, min(LENGTH - player.rect.height, player.rect.y))
        
        # Scrolling background
        y += 6  # How fast it scrolls
        finish_line_y += 6
        if finish_line_y > LENGTH:
            finish_line_y = LENGTH
        if y >= LENGTH:
            y = 0
        window.blit(background, (x, y))
        window.blit(background, (x, y - LENGTH))
        
        # draw sprites
        all_sprites.update()
        all_sprites.draw(window)
        
        # Finish line
        finish_line = pygame.Rect(0, finish_line_y, 800, 25)
        
        # player/obstacle collision
        collided_obstacles = pygame.sprite.spritecollide(player, obstacle_group, dokill=False)
        for obstacle in collided_obstacles:
            obstacle.kill()  # remove obstacle after hitting it
            lives -= 1 
        
        if player.rect.colliderect(finish_line):
            you_win_screen()
        
        # Check if lives ran out
        if lives <= 0:
            game_over_screen()  
        
        
        # Display lives
        lives_text = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = lives_text.render('Lives: ' + str(lives), False, (0, 255, 0))
        window.blit(text_surface, (5, 560))
        
        # Draw finish line
        pygame.draw.rect(window, BLUE, finish_line)
        
        pygame.display.flip()

    
def main():
    while True:
        show_start_screen()
        game_loop()
        
        
if __name__ == "__main__":
    main()
            
    
  
            