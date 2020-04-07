import pygame
import random
from bubble2 import Bubble
import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(filename='logfile.log', level=logging.INFO)


STARTING_BLUE_BUBBLE = 10
STARTING_RED_BUBBLE = 10
STARTING_GREEN_BUBBLE = 8

WIDTH = 800
HEIGHT = 800
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

game_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bubbles')
clock = pygame.time.Clock()


class Blue_bubble(Bubble):
    def __init__(self, x_boundary, y_boundary):
        Bubble.__init__(self, (0, 0, 255), x_boundary, y_boundary)

    def __add__(self, other_bubbles):
        logging.info('Bubble add op: {} + {}'.format(str(self.color), str(other_bubbles.color)))
        if other_bubbles.color == (255, 0, 0):
            self.size -= other_bubbles.size
            other_bubbles.size = 0

        elif other_bubbles.color == (0, 255, 0):
            self.size += other_bubbles.size
            other_bubbles.size = 0

        elif other_bubbles.color == (0, 0, 255):
            pass

        else:
            raise Exception('Tried to combine one or more multiple bubbles of unsupported colors.........!')


class Red_bubble(Bubble):
    def __init__(self, x_boundary, y_boundary):
        Bubble.__init__(self, (255, 0, 0), x_boundary, y_boundary)


class Green_bubble(Bubble):
    def __init__(self, x_boundary, y_boundary):
        Bubble.__init__(self, (0, 255, 0), x_boundary, y_boundary)


def is_touching(b1, b2):
    return np.linalg.norm(np.array([b1.x, b1.y])-np.array([b2.x, b2.y])) < (b1.size + b2.size)


def handle_collisions(bubble_list):
    blues, reds, greens = bubble_list
    for blue_id, blue_bubble in blues.copy().items():
        for other_bubbles in blues, reds, greens:
            for other_bubble_id, other_bubble in other_bubbles.copy().items():
                logging.debug('checking if bubbles are touching {} + {}'.format(str(blue_bubble.color), str(other_bubble.color)))
                if blue_bubble == other_bubble:
                    pass
                else:
                    if is_touching(blue_bubble, other_bubble):
                        blue_bubble + other_bubble
                        if other_bubble.size <= 0:
                            del other_bubbles[other_bubble_id]
                        if blue_bubble.size <= 0:
                            del blues[blue_id]
    return blues, reds, greens


def draw_env(bubble_list):
    game_display.fill(WHITE)
    blues, reds, greens = handle_collisions(bubble_list)

    for bubble_dict in bubble_list:
        for bubble_id in bubble_dict:
            bubble = bubble_dict[bubble_id]
            pygame.draw.circle(game_display, bubble.color, [bubble.x, bubble.y], bubble.size)
            bubble.move()
            bubble.check_bounds()
    pygame.display.update()
    return blues, reds, greens


def main():
    blue_bubbles = dict(enumerate([Blue_bubble( WIDTH, HEIGHT) for i in range(STARTING_BLUE_BUBBLE)]))
    red_bubbles = dict(enumerate([Red_bubble( WIDTH, HEIGHT) for i in range(STARTING_RED_BUBBLE)]))
    green_bubbles = dict(enumerate([Green_bubble( WIDTH, HEIGHT) for i in range(STARTING_GREEN_BUBBLE)]))

    print('current blue size: {}. curent red size: {}'.format(str(blue_bubbles[0].size),
                                                              str(red_bubbles[0].size)))

    print('Current blue size: {}. Current red size: {}'.format(str(blue_bubbles[0].size),
                                                               str(red_bubbles[0].size)))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        blue_bubbles, red_bubbles, green_bubbules = draw_env([blue_bubbles, red_bubbles, green_bubbles])
        clock.tick(60)


if __name__ == '__main__':
    main()



