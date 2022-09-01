import pygame
import sys
from settings import *


#PYGAME INIT
pygame.init()


def draw_floor():
    screen.blit(floor, (fx, 550))
    screen.blit(floor, (fx + 416, 550))


#WINDOW
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird")

#BIRD
bird_img = pygame.image.load("Graphics/bluebird-midflap.png").convert_alpha()
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

        #FLOOR MOVE
        fx -= 1
        if fx < -416:
            fx = 0

        #BIRD MOVE
        bird_move += gravity
        bird_rect.centery += bird_move

        #IMAGES
        screen.blit(background, (0, 0))
        screen.blit(bird_img, bird_rect)
        draw_floor()

        #WINDOW UPDATE
        pygame.display.update()
        clock.tick(FRAMERATE)