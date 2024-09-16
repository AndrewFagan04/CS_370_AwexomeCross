

import pygame
import random
import sys

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('game')

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)

# Stars settings
num_stars = 100
stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)] for _ in range(num_stars)]

clock = pygame.time.Clock()
game_over = False

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)


def update_and_draw_stars(stars):
    for star in stars:
        star[1] += star[2]  # Move star downward based on its size (speed)
        if star[1] > HEIGHT:  # Reset star to top once it goes off-screen
            star[0] = random.randint(0, WIDTH)
            star[1] = 0
        pygame.draw.circle(screen, WHITE, (star[0], star[1]), star[2])  # Draw star

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    

    # Fill screen with background color
    screen.fill(BACKGROUND_COLOR)
    
    # Update and draw stars to create a moving starfield
    update_and_draw_stars(stars)

    # Update the display
    pygame.display.flip()

    # Control fps
    clock.tick(30)

pygame.display.flip()
pygame.time.wait(2000)
pygame.quit()
