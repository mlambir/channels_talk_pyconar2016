import random
from math import sin

import pygame

from utils import COLORS, get_sprite_surface


class LostState(object):
    def __init__(self, surface, score):
        self.surface = surface
        self.score = score
        self.y = 0
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.offsets = [0] * self.width

        self.score_font = pygame.font.Font('fonts/prstart.ttf', 8)

        txt = "SCORE: {0:06d}".format(self.score)
        self.restart = False

        self.score_text_surfaces = []
        for c in txt:
            t_w, t_h = self.score_font.size(c)
            surf = pygame.Surface((t_w + 1, t_h + 1))
            surf.blit(self.score_font.render(c, False, COLORS[3]), (1, 1))
            surf.blit(self.score_font.render(c, False, COLORS[1]), (0, 0))
            surf.set_colorkey(0)
            self.score_text_surfaces.append(surf)
        self.score_width = sum(s.get_width() for s in self.score_text_surfaces)
        self.score_height = max(s.get_height() for s in self.score_text_surfaces)

    def get_next_state(self):
        if self.restart:
            from game_state import GameState
            return GameState(self.width, self.height)
        return self

    def update(self, selected):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.restart = True
        self.offsets = [o + random.choice([1, 2, 5]) for o in self.offsets]

    def draw(self, buffer):
        buffer.fill(COLORS[2])
        base_x = (self.width - self.score_width) / 2
        base_y = (self.height - self.score_height) / 3
        t = pygame.time.get_ticks() / 100

        for n, s in enumerate(self.score_text_surfaces):
            buffer.blit(s, (base_x, base_y + 3 * sin(t + n)))
            base_x += s.get_width()


        if t % 10 > 5:
            retry = "RETRY?"
            w, h = self.score_font.size(retry)
            x = (self.width - w) / 2
            y = (self.height - h) * 2 / 3

            buffer.blit(self.score_font.render(retry, False, COLORS[3]), (x + 1, y + 1))
            buffer.blit(self.score_font.render(retry, False, COLORS[1]), (x, y))

        for x, offset in enumerate(self.offsets):
            if offset < self.height:
                buffer.blit(self.surface, (x, offset), (x, 0, 1, self.height))
