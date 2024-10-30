import pygame
import sys
import random
import time
import cv2
from os.path import join

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
fps = 60

class Button:
    def __init__(self, x, y, width, height, color, play):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.play = play
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        play_surf = self.font.render(self.play, True, BLUE)
        play_rect = play_surf.get_rect(center=self.rect.center)
        surface.blit(play_surf, play_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def show_start_screen(WIDTH, LENGTH, window, game_loop):
    play_button = Button(WIDTH // 2 - 100, LENGTH // 2 - 25, 200, 50, GREEN, "Play")
    my_font = pygame.font.SysFont('Comic Sans MS', 60)

    high_score_button = Button(WIDTH // 2 - 100, LENGTH // 2 + 50, 200, 50, GREEN, "High Scores")
    my_font = pygame.font.SysFont('Comic Sans MS', 60)
    
    while True:
        window.fill(RED)
        start_surface = my_font.render('Awesome Cross V2', False, (0, 0, 0)) #play
        start_rect = start_surface.get_rect(center = (WIDTH/2, LENGTH / 2 - 80)) #created rect for the play to center it
        window.blit(start_surface, start_rect) 
        play_button.draw(window)
        high_score_button.draw(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(event.pos):
                    cutscene(join('Cycle_2',"testvideo.mp4"), window)
                    game_loop()
                if high_score_button.is_clicked(event.pos):
                    high_score_screen(WIDTH, LENGTH, window, game_loop)
        
        pygame.display.flip()
        pygame.time.Clock().tick(fps)
 
      
def game_over_screen(WIDTH, LENGTH, window, game_loop):
    replay_button = Button(WIDTH // 2 - 100, LENGTH // 2 - 25, 200, 50, GREEN, "Try again")
    my_font = pygame.font.SysFont('Comic Sans MS', 60)
    while True:
        window.fill(RED)
        play_surface = my_font.render('Game Over!', False, (0, 0, 0))
        play_rect = play_surface.get_rect(center = (WIDTH/2, LENGTH / 2 - 80)) #created rect for the play to center it
        window.blit(play_surface, play_rect)
        replay_button.draw(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.is_clicked(event.pos):
                    game_loop() 
        
        pygame.display.flip()
        pygame.time.Clock().tick(fps)
        
def you_win_screen(WIDTH, LENGTH, window, game_loop):
    play_button = Button(WIDTH // 2 - 100, LENGTH // 2 - 25, 200, 50, GREEN, "Play Again")
    my_font = pygame.font.SysFont('Comic Sans MS', 60)
    while True:
        window.fill(RED)
        play_surface = my_font.render('You Win!', False, (0, 0, 0))
        play_rect = play_surface.get_rect(center = (WIDTH/2, LENGTH / 2 - 80)) #created rect for the play to center it
        window.blit(play_surface, play_rect)
        play_button.draw(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(event.pos):
                    game_loop()
        
        pygame.display.flip()
        pygame.time.Clock().tick(fps)

def high_score_screen(WIDTH, LENGTH, window, game_loop):
    start_screen_button = Button(WIDTH / 2 - 100, LENGTH - 100, 200, 50, GREEN, "Return")
    my_font = pygame.font.SysFont('Comic Sans MS', 60)
    
    while True:
        window.fill(RED)
        score_surface = my_font.render('High Scores', False, (0, 0, 0)) #play
        score_rect = score_surface.get_rect(center = (WIDTH/2, 50)) #created rect for the play to center it
        window.blit(score_surface, score_rect) 
        start_screen_button.draw(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_screen_button.is_clicked(event.pos):
                    show_start_screen(WIDTH, LENGTH, window, game_loop)
        
        pygame.display.flip()
        pygame.time.Clock().tick(fps)


def cutscene(video_path, window):
    # videocapture thing from cv2
    cap = cv2.VideoCapture(join('Cycle_2',"testvideo.mp4"))

    clock = pygame.time.Clock()
    fps = 30  

    #when the video is running
    while cap.isOpened():
        ret, frame = cap.read()
        
        # if no frames read, the video ends
        if not ret:
            break
        
        #if you need to rotate the video, use this
        #frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        # convert to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # pygame surface
        frame_surface = pygame.surfarray.make_surface(frame_rgb)
        
        # if you need to scale it
        frame_surface = pygame.transform.scale(frame_surface, (window.get_width(), window.get_height()))
        
        # Display to window
        window.blit(frame_surface, (0, 0))
        pygame.display.flip()
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        clock.tick(fps)
    
    # release and close video after played
    cap.release()
    pygame.display.flip()
    
