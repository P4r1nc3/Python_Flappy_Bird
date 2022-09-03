import pygame
import sys
import random
from settings import *

# PYGAME INIT
pygame.init()


def pipe_animation():
    global game_over, is_score_time
    for pipe in PIPES:
        if pipe.top < 0:
            flipped_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flipped_pipe, pipe)
        else:
            screen.blit(pipe_img, pipe)
        pipe.centerx -= 3

        if pipe.right < 0:
            PIPES.remove(pipe)

        if bird_rect.colliderect(pipe):
            game_over = True
            is_score_time = True


def draw_floor():
    screen.blit(floor, (fx, 530))
    screen.blit(floor, (fx + 416, 530))


def draw_pipe():
    pipe_y = random.choice(pipe_height)
    top_pipe = pipe_img.get_rect(midbottom=(467, pipe_y - 200))
    bottom_pipe = pipe_img.get_rect(midtop=(467, pipe_y))
    return top_pipe, bottom_pipe


def draw_score(game_state):
    if game_state == "game_on":
        score_text = score_font.render(str(score), True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 66))
        screen.blit(score_text, score_rect)
    elif game_state == "game_over":
        score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 66))
        screen.blit(score_text, score_rect)

        high_score_text = score_font.render(f"High Score: {high_score}", True, (255, 255, 255))
        high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, 506))
        screen.blit(high_score_text, high_score_rect)


def update_score():
    global score, is_score_time, high_score
    if PIPES:
        for pipe in PIPES:
            if 65 < pipe.centerx < 69 and is_score_time:
                score += 1
                is_score_time = False

            if pipe.left <= 0:
                is_score_time = True

    if score > high_score:
        high_score = score


# WINDOW
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# BIRD
bird_up = pygame.image.load("Graphics/bluebird-upflap.png")
bird_mid = pygame.image.load("Graphics/bluebird-midflap.png")
bird_down = pygame.image.load("Graphics/bluebird-downflap.png")

BIRDS = [bird_up, bird_mid, bird_down]
bird_index = 0
BIRD_FLAP = pygame.USEREVENT
pygame.time.set_timer(BIRD_FLAP, 200)

bird_img = BIRDS[bird_index]
bird_rect = bird_img.get_rect(center=(70, 622 / 2))
bird_move = 0
gravity = 0.17

# PIPES
pipe_img = pygame.image.load("Graphics/pipe-green.png").convert_alpha()
pipe_height = [250, 350, 450, 300]

PIPES = []
CREATE_PIPES = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_PIPES, 1200)

# GAME OVER
game_over = True
game_over_img = pygame.image.load("Graphics/message.png").convert_alpha()
game_over_rect = game_over_img.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

# BACKGROUND
background = pygame.image.load("Graphics/background-day.png").convert()

# FLOOR
floor = pygame.image.load("Graphics/base.png").convert()
fx = 0

# SCORE
score = 0
high_score = 0
is_score_time = True

# FONT
score_font = pygame.font.Font("Fonts/04B_19.ttf", 27)

# CLOCK
clock = pygame.time.Clock()

# GAME LOOP
while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_move = 0
                bird_move = -6

            if event.key == pygame.K_SPACE and game_over:
                game_over = False
                PIPES = []
                bird_move = 0
                bird_rect = bird_img.get_rect(center=(67, 622 // 2))
                is_score_time = True
                score = 0

        if event.type == BIRD_FLAP:
            bird_index += 1

            if bird_index > 2:
                bird_index = 0

            bird_image = BIRDS[bird_index]
            bird_rect = bird_image.get_rect(center=bird_rect.center)

        if event.type == CREATE_PIPES:
            PIPES.extend(draw_pipe())

    screen.blit(background, (0, 0))
    if not game_over:
        bird_move += gravity
        bird_rect.centery += bird_move
        rotated_bird = pygame.transform.rotozoom(bird_img, bird_move * -6, 1)

        if bird_rect.top <= 5:
            game_over = True

        if bird_rect.bottom >= 530:
            game_over = True

        screen.blit(rotated_bird, bird_rect)
        pipe_animation()
        update_score()
        draw_score("game_on")
    elif game_over:
        draw_score("game_over")
        screen.blit(game_over_img, game_over_rect)

    # FLOOR MOVE
    fx -= 1
    if fx < -448:
        fx = 0

    draw_floor()
    pygame.display.update()
    clock.tick(FRAMERATE)
