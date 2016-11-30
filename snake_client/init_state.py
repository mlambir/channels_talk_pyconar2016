from math import sin

import pygame
from noise import snoise2

from utils import COLORS

octaves = 4
freq = 32.0 * octaves


def _get_noise_val(x, y, t):
    return snoise2((x + t) / freq, (y + t / 5) / freq, octaves)


class InitState(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.start = False
        self.t = 0
        self.title_font = pygame.font.Font('fonts/upheavtt.ttf', 20)

        txt = "PYCON SNAKE"
        self.title_text_surfaces = []
        for c in txt:
            t_w, t_h = self.title_font.size(c)
            surf = pygame.Surface((t_w + 1, t_h + 1))
            surf.blit(self.title_font.render(c, False, COLORS[3]), (1, 1))
            surf.blit(self.title_font.render(c, False, COLORS[0]), (0, 0))
            surf.set_colorkey(0)
            self.title_text_surfaces.append(surf)
        self.title_width = sum(s.get_width() for s in self.title_text_surfaces)
        self.title_height = max(s.get_height() for s in self.title_text_surfaces)

    def get_next_state(self):
        if self.start:
            from game_state import GameState
            return GameState(self.width, self.height)
        return self

    def update(self, selected):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.start = True

    def draw(self, buffer):
        t = pygame.time.get_ticks() / 100

        for x in range(self.width):
            for y in range(self.height):
                color = _get_noise_val(x, y, self.t)
                if color < -.4:
                    buffer.set_at((x, y), COLORS[1])
                elif color < 0:
                    if (x + y) % 2 == 0:
                        buffer.set_at((x, y), COLORS[1])
                    else:
                        buffer.set_at((x, y), COLORS[2])
                elif color < .3:
                    if (x + y) % 3 == 0:
                        buffer.set_at((x, y), COLORS[1])
                    else:
                        buffer.set_at((x, y), COLORS[2])
                else:
                    if (x + y) % 5 == 0:
                        buffer.set_at((x, y), COLORS[1])
                    else:
                        buffer.set_at((x, y), COLORS[2])

        self.t += .2

        base_x = (self.width - self.title_width) / 2
        base_y = (self.height - self.title_height) / 2

        for n, s in enumerate(self.title_text_surfaces):
            buffer.blit(s, (base_x, base_y + 3 * sin(t + n)))
            base_x += s.get_width()