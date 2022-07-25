import sys
from random import randint

import pygame
from pygame import gfxdraw

WIN_SIZE = WIDTH, HEIGHT = 1440, 900
STEPS_BETWEEN_COLORS = 9
COLORS = ['black', 'red', 'orange', 'yellow', 'white']
PIXEL_SIZE = 4
FIRE_REPS = 4
FIRE_WIDTH = WIDTH // (PIXEL_SIZE * FIRE_REPS)
FIRE_HEIGHT = HEIGHT // (PIXEL_SIZE)

pygame.init()


class HellFire:
    def __init__(self, app):
        self.app = app
        self.palette = self.get_palette()
        self.fire_array = self.get_fire_array()
        self.fire_surf = pygame.Surface(
            [PIXEL_SIZE * FIRE_WIDTH, PIXEL_SIZE * FIRE_HEIGHT])
        self.fire_surf.set_colorkey('black')
        self.logo = pygame.image.load('hellfireclub.png')
        self.logo_x, self.logo_y = (WIDTH // 2 - self.logo.get_width() // 2,
                                    HEIGHT // 3 - self.logo.get_height() // 2)
        self.logo_start_y = HEIGHT

    def draw_logo(self):
        if self.logo_start_y > self.logo_y:
            self.logo_start_y -= 5
        self.app.screen.blit(self.logo, (self.logo_x, self.logo_start_y))

    def do_fire(self):
        for x in range(FIRE_WIDTH):
            for y in range(1, FIRE_HEIGHT):
                color_index = self.fire_array[y][x]
                if color_index:
                    rnd = randint(0, 3)
                    self.fire_array[y-1][(x - rnd + 1) % FIRE_WIDTH] = color_index - rnd % 2
                else:
                    self.fire_array[y-1][x] = 0

    def draw_fire(self):
        self.fire_surf.fill('black')
        for y, row in enumerate(self.fire_array):
            for x, color_index in enumerate(row):
                if color_index:
                    color = self.palette[color_index]
                    gfxdraw.box(
                        self.fire_surf,
                        (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE,
                         PIXEL_SIZE),
                        color
                    )
        for i in range(FIRE_REPS):
            self.app.screen.blit(
                self.fire_surf, (self.fire_surf.get_width()*i, 0)
            )

    def get_fire_array(self):
        fire_array = [[0 for i in range(FIRE_WIDTH)] for j in
                      range(FIRE_HEIGHT)]
        for i in range(FIRE_WIDTH):
            fire_array[FIRE_HEIGHT - 1][i] = len(self.palette) - 1
        return fire_array

    def draw_palette(self):
        size = 90
        for i, color in enumerate(self.palette):
            pygame.draw.rect(
                self.app.screen, color,
                (i * size, HEIGHT // 2, size - 5, size - 5))

    @staticmethod
    def get_palette():
        palette = [(0, 0, 0)]
        for i, color in enumerate(COLORS[:-1]):
            c1, c2 = color, COLORS[i + 1]
            for step in range(STEPS_BETWEEN_COLORS):
                c = pygame.Color(c1).lerp(c2,
                                          (step + .5) / STEPS_BETWEEN_COLORS)
                palette.append(c)
        return palette

    def update(self):
        self.do_fire()

    def draw(self):
        # self.draw_palette()
        self.draw_logo()
        self.draw_fire()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(WIN_SIZE)
        self.clock = pygame.time.Clock()
        self.hell_fire = HellFire(self)

    def update(self):
        self.hell_fire.update()
        self.clock.tick(60)
        pygame.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw(self):
        self.screen.fill('#0f0f0f')
        self.hell_fire.draw()
        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.update()
            self.draw()


Game().run()
