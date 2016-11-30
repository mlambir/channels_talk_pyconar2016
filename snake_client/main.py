import json
from threading import Thread

import pygame
import websocket
import time

from math import floor

from init_state import InitState
from utils import COLORS, get_sprite_surface

console_size = console_width, console_height = 320, 240
console_size_final = console_width * 4, console_height * 4
pixel_size = width, height = 160, 144
screen_size = (width * 4, height * 4)

ARROW = [
    [0, 0, 0, 3, 0, 0, 0],
    [0, 0, 3, 3, 3, 0, 0],
    [0, 3, 3, 3, 3, 3, 0],
    [3, 3, 3, 3, 3, 3, 3],
    [0, 0, 3, 3, 3, 0, 0],
    [0, 0, 3, 3, 3, 0, 0],
    [0, 0, 3, 3, 3, 0, 0],
]

values = {
    "up": 20,
    "down": 10,
    "left": 0,
    "right": 50,

    "connected": 100,
    "selected": "up"
}


def on_message(ws, message):
    global values
    values = json.loads(message)

def on_close(ws):
    print("### closed ###")

websocket.enableTrace(True)
ws = websocket.WebSocketApp("ws://0.0.0.0:8000/", on_message=on_message, on_close=on_close)
wst = Thread(target=ws.run_forever)
wst.daemon = True
wst.start()

conn_timeout = 5
while not ws.sock.connected and conn_timeout:
    time.sleep(1)
    conn_timeout -= 1


def main():
    global values
    msg_counter = 0

    """ Set up the game and run the main game loop """
    pygame.init()

    clock = pygame.time.Clock()

    main_surface = pygame.display.set_mode(console_size_final)
    main_surface.fill(pygame.Color(100, 100, 100))
    buffer = pygame.Surface(pixel_size)

    arrows_buffer = pygame.Surface((100, 144))

    state = InitState(width, height)

    font = pygame.font.Font('fonts/prstart.ttf', 8)

    arrow_up = get_sprite_surface(ARROW)
    arrow_up.set_colorkey(COLORS[0])

    arrows = {
        'up': arrow_up,
        'down': pygame.transform.rotate(arrow_up, 90 * 2),
        'left': pygame.transform.rotate(arrow_up, 90),
        'right': pygame.transform.rotate(arrow_up, 90*3),
    }

    big_arrows = {k: pygame.transform.scale2x(v) for k, v in arrows.items()}

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break

        selected = values["selected"]

        state.update(selected)
        state.draw(buffer)
        state = state.get_next_state()

        buffer.set_alpha(110)
        main_surface.blit(pygame.transform.scale(buffer, screen_size), (40, 40))

        arrows_buffer.fill(COLORS[0])

        y = 4
        x = 4

        for i in 'up', 'down', 'left', 'right':
            txt = "{0:06d}".format(values[i])
            x = 4
            arrows_buffer.blit(arrows[i], (x, y))
            x += arrows[i].get_width() + 4
            arrows_buffer.blit(font.render(txt, False, COLORS[2]), (x, y))
            y += font.size(txt)[1]

        y +=10

        x = (arrows_buffer.get_width() - big_arrows['up'].get_width())/2
        if selected == 'up':
            pygame.draw.circle(arrows_buffer, COLORS[1], (floor(x + big_arrows['up'].get_width()/2), floor(y + big_arrows['up'].get_height()/2)), 10)
        arrows_buffer.blit(big_arrows['up'], (x, y))

        y += 10 + big_arrows['up'].get_height()
        x = (arrows_buffer.get_width() - big_arrows['up'].get_width()*4)/2
        if selected == 'left':
            pygame.draw.circle(arrows_buffer, COLORS[1], (floor(x + big_arrows['up'].get_width()/2), floor(y + big_arrows['up'].get_height()/2)), 10)
        arrows_buffer.blit(big_arrows['left'], (x, y))

        x = (arrows_buffer.get_width() + big_arrows['up'].get_width()*2)/2
        if selected == 'right':
            pygame.draw.circle(arrows_buffer, COLORS[1], (floor(x + big_arrows['up'].get_width()/2), floor(y + big_arrows['up'].get_height()/2)), 10)
        arrows_buffer.blit(big_arrows['right'], (x, y))

        y += 10 + big_arrows['up'].get_height()
        x = (arrows_buffer.get_width() - big_arrows['up'].get_width())/2
        if selected == 'down':
            pygame.draw.circle(arrows_buffer, COLORS[1], (floor(x + big_arrows['up'].get_width()/2), floor(y + big_arrows['up'].get_height()/2)), 10)
        arrows_buffer.blit(big_arrows['down'], (x, y))


        arrows_buffer.set_alpha(110)
        main_surface.blit(pygame.transform.scale(arrows_buffer, (100 * 4, 144 * 4)), (screen_size[0] + 40 * 2, 40))
        pygame.display.flip()

        # ws.send('Hello world %d' % msg_counter)
        msg_counter += 1

        clock.tick(30)

    pygame.quit()  # Once we leave the loop, close the window.


main()
