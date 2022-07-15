import os
import sys

import pygame
from pygame.rect import Rect

pygame.init()

fpsclock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Bricks')

background = pygame.color.Color(100, 149, 237)
BLACK = pygame.color.Color(0, 0, 0)

# bat init
bat = pygame.image.load('bat.png')
playerY = 540
bat_rect = bat.get_rect()
mousex, mousey = (0, playerY)

# ball init
ball = pygame.image.load('ball.png')
ball_rect = ball.get_rect()
ball_startY = 200
ball_speed = 3
ball_served = False
bx, by = (0, ball_startY)
sx, sy = (ball_speed, ball_speed)
ball_rect.topleft = bx, by
# brick init
brick = pygame.image.load('brick.png')
bricks = []
for y in range(5):
    brickY = (y * 24) + 100
    for x in range(10):
        brickX = (x * 31) + 245
        width = brick.get_width()
        height = brick.get_height()
        rect = Rect(brickX, brickY, width, height)
        bricks.append(rect)


while True:
    screen.fill(BLACK)

    # brick draw
    for b in bricks:
        screen.blit(brick, b)
    # bat and ball draw
    screen.blit(bat, bat_rect)
    screen.blit(ball, ball_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            mousex, mousey = event.pos
            if mousex < 800 - 55:
                bat_rect.topleft = mousex, playerY
            else:
                bat_rect.topleft = 800-55, playerY
        elif event.type == pygame.MOUSEBUTTONUP and not ball_served:
            ball_served = True

    # main game logic
    if ball_served:
        bx += sx
        by += sy
        ball_rect.topleft = bx, by
    if by <= 0:
        by = 0
        sy *= - 1
    if by >= 600 - 8:
        by = 600 - 8
        sy *= -1
    if bx <= 0:
        bx = 0
        sx *= -1
    if bx >= 800 - 8:
        bx = 800 - 8
        sx *= -1
    # collision detection
    if ball_rect.colliderect(bat_rect):
        by = playerY - 8
        sy *= -1

    pygame.display.update()
    fpsclock.tick(60)

