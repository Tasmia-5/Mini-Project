import pygame
import random
import math
import sys
import os
from os import listdir
from os.path import isfile, join
from frog import *
from duck import *

"""
WIDTH = 1000
HEIGHT = 500
FPS = 60
PLAYER_VEL = 5
"""
# test files for now but will be for the game

pygame.init()
pygame.display.set_caption("Platformer")
WIDTH, HEIGHT = 1000, 500
FPS = 60
PLAYER_VEL = 5
window = pygame.display.set_mode((WIDTH, HEIGHT))


def get_background(name):
    image = pygame.image.load(join("resources", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []


def main(window):
    # the game itself
    clock = pygame.time.Clock()
    game = True
    while run:
        clock.tick.Clock(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                break
    pygame.quit()
    quit()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # play = Button(1000 / 2 - 15, 250, "[ START ]", screen)


# download pygame package
# for both duck and frog, board
class Forjobday:
    def __init__(self, size, remove_frog, add_face, duck, face, messages, add_messages):
        self.remove_frog = remove_frog
        self.add_face = add_face
        self.duck = duck
        self.face = face
        self.size = size

        def remove_frog(self):
            return self.remove_frog

        def add_face(self):
            return add_face


def generate_app(size, add_face, self=None):
    self.size = size
    pass


def messages(self, add_messages):
    return self
    return add_messages
    self.add_messages
    pass


def generate_app(size, screen):
    return size
    return screen
    pass


def add_face(self):
    return self
    pass


def remove_frog(self):
    return self
    pass


def add_messages(self):
    return self
    pass


if __name__ == '__main__':
    main()
