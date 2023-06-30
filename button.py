"""import os
import random
import math"""
import pygame
from os import listdir
from os.path import isfile, join


class Button:
    def __init__(self, x, y, text, screen):
        self.screen = screen
        self.text = text
        self.x = x
        self.y = y

        self.gameFont = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.text_width, self.text_height = self.gameFont.size(f"{self.text}")
        self.buttonText = self.gameFont.render(str(self.text), True, "black", "white")
        self.rect = pygame.Rect(self.x - 6, self.y - 6, self.text_width + 12, self.text_height + 9)


def draw_start_menu(screen):
    # lilac message, black font
    # menu/buttons
    # baby blue hex = #89CFF0, RGB = (137, 207, 240)
    # lighter baby blue hex = #A5DCF0, RGB = (165, 220, 240)
    # very dark blue RGB = (68, 85, 90)
    BLUE = pygame.Color("#89CFF0")
    BLACK = (13, 13, 13)
    YOLK = (252, 232, 131)
    FROGGE = (147, 197, 114)
    WIDTH = 1000
    HEIGHT = 500
    FPS = 60
    PLAYER_VEL = 5
    screen.fill(BLUE)

    # draw buttons
    button_font = pygame.font.Font(None, 50)
    duck_text = button_font.render("DUCK", 0, BLACK)
    frog_text = button_font.render("FROG", 0, BLACK)

    # make button boxes
    duck_box = pygame.Surface(
        (duck_text.get_size()[0] + 20, duck_text.get_size()[1] + 20))
    frog_box = pygame.Surface(
        (frog_text.get_size()[0] + 20, frog_text.get_size()[1] + 20))
    duck_box.fill(FROGGE)
    frog_box.fill(YOLK)

    # draw text on boxes
    duck_box.blit(duck_text, (10, 10))
    frog_box.blit(frog_text, (10, 10))

    # button size
    duck_rectangle = duck_box.get_rect(
        center=(WIDTH // 2 - 50, HEIGHT // 2 + 100))
    frog_rectangle = frog_box.get_rect(
        center=(WIDTH // 2 - 50, HEIGHT // 2 + 200))

    # draw buttons into bg
    screen.blit(duck_box, duck_rectangle)
    screen.blit(frog_box, frog_rectangle)

    pygame.display.flip()

    # connect buttons to main


# https://www.youtube.com/watch?v=N6xqCwblyiw
# https://www.youtube.com/watch?v=B6DrRN5z_uU (current one)
# https://www.youtube.com/watch?v=MYaxPa_eZS0 (sprite tutorial)
