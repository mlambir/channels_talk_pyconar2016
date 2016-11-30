import random

import pygame
from utils import COLORS, get_sprite_surface

SNAKE_HEAD = [[0, 0, 0, 3, 3, 0, 0, 0],
              [0, 0, 3, 2, 2, 3, 0, 0],
              [0, 3, 2, 2, 2, 2, 3, 0],
              [0, 3, 3, 2, 2, 3, 3, 0],
              [3, 1, 1, 3, 3, 1, 1, 3],
              [3, 1, 1, 3, 3, 1, 1, 3],
              [0, 3, 3, 2, 2, 3, 3, 0],
              [0, 0, 3, 3, 3, 3, 0, 0]]

SNAKE_BODY = [[0, 3, 3, 0],
              [3, 2, 2, 3],
              [3, 2, 2, 3],
              [0, 3, 3, 0]]

APPLE = [[0, 3, 3, 0],
         [3, 3, 3, 3],
         [3, 3, 3, 3],
         [0, 3, 3, 0]]


class GameState(object):
    def __init__(self, width, height):
        self.head_sprite = get_sprite_surface(SNAKE_HEAD)
        self.head_sprite.set_colorkey(COLORS[0])
        self.body_sprite = get_sprite_surface(SNAKE_BODY)
        self.body_sprite.set_colorkey(COLORS[0])
        self.apple_sprite = get_sprite_surface(APPLE)
        self.apple_sprite.set_colorkey(COLORS[0])

        self.score_font = pygame.font.Font('fonts/prstart.ttf', 8)

        self.width = width
        self.height = height

        self.game_width = width - 8
        self.game_height = height - 16
        self.game_x = 4
        self.game_y = 12

        self.apples = []
        self.snake_body = []
        self.snake_direction = None
        self.last_ticks = 0
        self.game_finished = False

        self.reset_game()

    def randomize_apple(self):
        while True:
            apple = (
                random.randint(0, (self.game_width / 4) - 1), random.randint(0, (self.game_height / 4) - 1))
            if not apple in self.snake_body:
                self.apples = [apple]
                return

    def reset_game(self):

        self.snake_body = [
            (self.game_width / 8, self.game_height / 8),
            (self.game_width / 8, self.game_height / 8 + 1),
        ]
        self.snake_direction = (0, -1)
        self.last_direction = self.snake_direction
        self.randomize_apple()
        self.last_ticks = pygame.time.get_ticks()
        self.update_ticks = 300
        self.score = 0

    def get_next_state(self):
        if self.game_finished:
            surface = pygame.Surface((self.width, self.height))
            self.draw(surface)
            from lost_state import LostState
            return LostState(surface, self.score)
        return self

    def update(self, selected):
        # keys = pygame.key.get_pressed()
        if selected == 'left' and self.last_direction != (1, 0):
            self.snake_direction = (-1, 0)
        if selected == 'right' and self.last_direction != (-1, 0):
            self.snake_direction = (1, 0)
        if selected == 'up' and self.last_direction != (0, 1):
            self.snake_direction = (0, -1)
        if selected == 'down' and self.last_direction != (0, -1):
            self.snake_direction = (0, 1)

        curr_ticks = pygame.time.get_ticks()

        if curr_ticks - self.last_ticks > self.update_ticks:
            self.last_direction = self.snake_direction
            self.updated = True
            self.last_ticks = curr_ticks

            new_head = (
                self.snake_body[0][0] + self.snake_direction[0], self.snake_body[0][1] + self.snake_direction[1])
            if new_head in self.snake_body or new_head[0] < 0 or new_head[1] < 0 or new_head[0] >= self.game_width / 4 or new_head[1] >= self.game_height / 4:
                self.game_finished = True
                return
            if new_head in self.apples:
                self.snake_body = [new_head] + self.snake_body
                self.randomize_apple()
                if self.update_ticks > 50:
                    self.update_ticks -= 50
                self.score += 100
            else:
                self.snake_body = [new_head] + self.snake_body[:-1]
        else:
            self.updated = False

    def draw(self, buffer):
        if self.updated:
            buffer.fill(COLORS[2])

            pygame.draw.rect(buffer, COLORS[0], (self.game_x, self.game_y, self.game_width, self.game_height))
            pygame.draw.rect(buffer, COLORS[3],
                             (self.game_x - 1, self.game_y - 1, self.game_width + 1, self.game_height + 1), 1)

            for x, y in self.apples:
                buffer.blit(self.apple_sprite, (self.game_x + x * 4,
                                                self.game_y + y * 4))
            if self.snake_direction == (1, 0):
                head_directed = pygame.transform.rotate(self.head_sprite, 90 * 3)
            if self.snake_direction == (-1, 0):
                head_directed = pygame.transform.rotate(self.head_sprite, 90)
            if self.snake_direction == (0, -1):
                head_directed = self.head_sprite
            if self.snake_direction == (0, 1):
                head_directed = pygame.transform.rotate(self.head_sprite, 90 * 2)

            for x, y in self.snake_body[1:]:
                buffer.blit(self.body_sprite, (self.game_x + x * 4, self.game_y + y * 4))
            buffer.blit(head_directed, (self.game_x + self.snake_body[0][0] * 4 - 2,
                                        self.game_y + self.snake_body[0][1] * 4 - 2))

            txt = "SCORE: {0:06d}".format(self.score)
            buffer.blit(self.score_font.render(txt, False, COLORS[3]), (self.game_x + 1, 3))
            buffer.blit(self.score_font.render(txt, False, COLORS[1]), (self.game_x, 2))
