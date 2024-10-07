# <insert collisionWASD.py here>
from collisionWASD import *

# Lives system
lives = 3  # Start with 3 lives

running = True
while running:
    timer.tick(fps)

    # Scrolling background
    # y += 3 #how fast it scrolls
    # if y == LENGTH:
    #     y = 0
    window.blit(background, (x, y))
    # window.blit(background, (x, y - LENGTH))

    # Character circle (change to sprite later)
    character = pygame.draw.circle(window, [255, 0, 0], [character_x, character_y], character_radius, 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Moving side to side
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        character_y -= speed
    if keys[pygame.K_a]:
        character_x -= speed
    if keys[pygame.K_s]:
        character_y += speed
    if keys[pygame.K_d]:
        character_x += speed

    # Borders so character doesn't move out of the screen   
    if character_x < WIDTH - WIDTH + character_radius:
        character_x = WIDTH - WIDTH + character_radius
    if character_x > WIDTH - character_radius:
        character_x = WIDTH - character_radius

    # Check collision and update lives
    col = GREEN
    for obstacle in obstacles:
        if character.colliderect(obstacle):
            col = RED
            lives -= 1  # Deduct a life on collision
            obstacles.remove(obstacle)  # Optional: remove the obstacle to avoid repeated collision
            break  # Exit loop after detecting collision

    # Check if lives are depleted
    if lives <= 0:
        print("Game Over!")  # we can replace this with an end game screen or restart logic
        running = False

    # Draw all rectangles  
    pygame.draw.rect(window, col, character)
    for obstacle in obstacles:
        pygame.draw.rect(window, BLUE, obstacle)

    # Display the number of lives
    font = pygame.font.Font(None, 36)
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    window.blit(lives_text, (10, 10))

    pygame.display.flip()
