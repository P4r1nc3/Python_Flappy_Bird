import pygame
import sys
from settings import *


#PYGAME INIT
pygame.init()

def draw_floor():
    screen.blit(floor, (fx, 510))
    screen.blit(floor, (fx + 416, 510))


#WINDOW
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird")

#BIRD
bird_up = pygame.image.load("Graphics/bluebird-upflap.png")
bird_mid = pygame.image.load("Graphics/bluebird-midflap.png")
bird_down = pygame.image.load("Graphics/bluebird-downflap.png")

BIRDS = [bird_up, bird_mid, bird_down]
bird_index = 0
BIRD_FLAP = pygame.USEREVENT
pygame.time.set_timer(BIRD_FLAP, 200)

bird_img = BIRDS[bird_index]
bird_rect = bird_img.get_rect(center = (70, 622/2))
bird_move = 0
gravity = 0.2

#BACKGROUND
background = pygame.image.load("Graphics/background-day.png").convert()

#FLOOR
floor = pygame.image.load("Graphics/base.png").convert()
fx = 0

#CLOCK
clock = pygame.time.Clock()

#GAME LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_move = 0
                bird_move -= 6

        if event.type == BIRD_FLAP:
            bird_index += 1

            if bird_index > 2:
                bird_index = 0

            bird_img = BIRDS[bird_index]
            bird_rect = bird_img.get_rect(center = bird_rect.center)

        #FLOOR MOVE
        fx -= 1
        if fx < -416:
            fx = 0

        #BIRD MOVE
        bird_move += gravity
        bird_rect.centery += bird_move
        bird_rotated = pygame.transform.rotozoom(bird_img, bird_move * -6, 1)

        #IMAGES
        screen.blit(background, (0, 0))
        screen.blit(bird_rotated, bird_rect)
        draw_floor()

        #WINDOW UPDATE
        pygame.display.update()
        clock.tick(FRAMERATE)