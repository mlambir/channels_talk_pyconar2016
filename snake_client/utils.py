import pygame


COLORS = [
    pygame.Color("#9bbc0f"),
    pygame.Color("#8bac0f"),
    pygame.Color("#306230"),
    pygame.Color("#0f380f")
]

COLORS = [
    pygame.Color("#FFFFFF"),
    pygame.Color("#AAAAAA"),
    pygame.Color("#555555"),
    pygame.Color("#222222"),
]


def get_sprite_surface(sprite_arr, transparent=None):
    width = len(sprite_arr[0])
    height = len(sprite_arr)

    surface = pygame.Surface((width, height))

    for y, rows in enumerate(sprite_arr):
        for x, color in enumerate(rows):
            if color != transparent:
                color = COLORS[color]
                surface.set_at((x, y), color)
    return surface
