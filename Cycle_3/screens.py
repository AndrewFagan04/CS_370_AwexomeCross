import pygame
import sys
import random
import time
import cv2
from endless import game_loop_endless
from main import *
from os.path import join

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 222, 33)
fps = 60

backgroundW = pygame.image.load(join("Cycle_3/sprites","AwexomeCrossTitleScreenY.png"))
backgroundY = pygame.image.load(join("Cycle_3/sprites","AwexomeCrossTitleScreenW.png"))
backgroundS = pygame.image.load(join("Cycle_3/sprites","space.png"))
moon = pygame.image.load(join("Cycle_3/sprites","8-bitMoonEND.png"))

class Button:
    def __init__(self, x, y, width, height, color, play):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.play = play
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        play_surf = self.font.render(self.play, True, WHITE)
        play_rect = play_surf.get_rect(center=self.rect.center)
        surface.blit(play_surf, play_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def show_start_screen(WIDTH, LENGTH, window, game_loop):
    play_button = Button(WIDTH // 2 - 250, LENGTH // 2 + 100, 200, 50, GREEN, "Play")
    my_font = pygame.font.SysFont('Comic Sans MS', 60)

    high_score_button = Button(WIDTH // 2 + 50, LENGTH // 2 + 100, 200, 50, BLUE, "High Scores")
    my_font = pygame.font.SysFont('Comic Sans MS', 60)
    
    while True:
        window.fill(RED)
        window.blit(backgroundW, (0,0))
        play_button.draw(window)
        high_score_button.draw(window)
        pygame.display.update()
        time.sleep(.1)
        window.blit(backgroundY, (0,0))
        play_button.draw(window)
        high_score_button.draw(window)
        pygame.display.update()
        time.sleep(.1)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(event.pos):
                    cutscene(join('Cycle_3',"testvideo.mp4"), window)
                    game_loop()
                if high_score_button.is_clicked(event.pos):
                    high_score_screen(WIDTH, LENGTH, window, game_loop)
        
        pygame.display.flip()
        pygame.time.Clock().tick(fps)
 
      
def game_over_screen(WIDTH, LENGTH, window, game_loop):
    replay_button = Button(WIDTH // 2 - 250, LENGTH // 2 - 25, 200, 50, RED, "Try again")
    menu_button = Button(WIDTH // 2 + 50, LENGTH // 2 - 25, 200, 50, RED, "Main Menu")
    my_font = pygame.font.SysFont('Comic Sans MS', 60)
    while True:
        window.fill(BLACK)
        window.blit(backgroundS, (0,0))
        play_surface = my_font.render('Game Over!', False, RED)
        play_rect = play_surface.get_rect(center = (WIDTH/2, LENGTH / 2 - 80)) #created rect for the play to center it
        window.blit(play_surface, play_rect)
        replay_button.draw(window)
        menu_button.draw(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.is_clicked(event.pos):
                    game_loop() 
                if menu_button.is_clicked(event.pos):
                    show_start_screen(WIDTH, LENGTH, window, game_loop) 
            
        
        pygame.display.flip()
        pygame.time.Clock().tick(fps)
        
def you_win_screen(WIDTH, LENGTH, window, game_loop):
    play_button = Button(WIDTH // 2 - 100, LENGTH // 2 - 25, 200, 50, GREEN, "Play Again")
    endless_button = Button(WIDTH // 2 - 100, LENGTH // 2 + 50, 200, 50, BLUE, "Endless Mode")  # Added endless mode button
    menu_button = Button(WIDTH // 2 - 100, LENGTH // 2 + 125, 200, 50, RED, "Main Menu")  # Main menu button
    my_font = pygame.font.SysFont('Comic Sans MS', 60)
    
    while True:
        window.fill(BLACK)
        window.blit(backgroundS, (0,0))
        window.blit(moon, (75,400))
        play_surface = my_font.render('You Win!', False, YELLOW)
        play_rect = play_surface.get_rect(center = (WIDTH/2, LENGTH / 2 - 80)) #created rect for the play to center it
        window.blit(play_surface, play_rect)
        
        # Draw the buttons
        play_button.draw(window)
        endless_button.draw(window)  # Draw the endless mode button
        menu_button.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(event.pos):
                    game_loop()  # Restart the game
                if endless_button.is_clicked(event.pos):
                    game_loop_endless()  # Start the endless mode
                if menu_button.is_clicked(event.pos):
                    window.show_start_screen(WIDTH, LENGTH, window, game_loop)  # Go back to the main menu
        
        pygame.display.flip()
        pygame.time.Clock().tick(fps)



def high_score_screen(WIDTH, LENGTH, window, game_loop):
    start_screen_button = Button(WIDTH / 2 - 100, LENGTH - 100, 200, 50, RED, "Return")
    my_font = pygame.font.SysFont('Comic Sans MS', 60)
    
    while True:
        window.fill(BLACK)
        score_surface = my_font.render('High Scores', False, WHITE) #play
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

def add_high_score(score_list,score):
    if(len(score_list) >= 5):
        if(score > score_list[4]):
            score_list.pop()
            score_list.append(score)
    else:
        score_list.append(score)
    score_list.sort()
    score_list.reverse()


def cutscene(video_path, window):
    # videocapture thing from cv2
    cap = cv2.VideoCapture(join('Cycle_3',"AwexomeCrossIntroCOMPETED.mp4"))

    clock = pygame.time.Clock()
    fps = 30  



    #when the video is running
    while cap.isOpened():
        ret, frame = cap.read()

        
        # if no frames read, the video ends
        if not ret:
            break
        
        #if you need to rotate the video, use this
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        
        #WIP
        #flips the video
        frame = cv2.flip(frame, 0)
        
        # convert to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # pygame surface
        frame_surface = pygame.surfarray.make_surface(frame_rgb)
        
        # if you need to scale it
        frame_surface = pygame.transform.scale(frame_surface, (900, 700))
        
        # Display to window
        window.blit(frame_surface, (-150, -50))
        pygame.display.flip()
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        clock.tick(fps)
    
    # release and close video after played
    cap.release()
    pygame.display.flip()
    
