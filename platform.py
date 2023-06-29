# -*- coding: utf-8 -*-
import pygame
import random
import math
import sys
import os
from os import listdir
from os.path import isfile, join
from pygame.mixer import*
# from frog import *
# from duck import *

"""
WIDTH = 1000
HEIGHT = 500
FPS = 60
PLAYER_VEL = 5
"""
# the game

pygame.init()
# the test file for now but will be for buttons
# using 'Characters' folder

BLUE = pygame.Color("#89CFF0")
BLACK = (13, 13, 13)
YOLK = (252, 232, 131)
FROGGE = (147, 197, 114)
WIDTH = 1000
HEIGHT = 500
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))


"""def draw_start_menu(window):
    # lilac message, black font
    # menu/buttons
    # baby blue hex = #89CFF0, RGB = (137, 207, 240)
    # lighter baby blue hex = #A5DCF0, RGB = (165, 220, 240)
    # very dark blue RGB = (68, 85, 90)
    # WIDTH = 1000
    # HEIGHT = 500
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
    window.blit(duck_box, duck_rectangle)
    window.blit(frog_box, frog_rectangle)

    pygame.display.flip()

    # connect buttons to main
"""
pygame.display.set_caption("Platformer")


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    SPRITES = load_sprite_sheets("Characters", "Duck", 32, 32, True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        # vel(s) = how fast player goes
        super().__init__()
        self.sprite = None
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        # fire
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["on"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)

    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    block_size = 96
    # Player(x axis posit...)
    # (...- block_size - "height", range of animation/sprite, bottom of object range)
    # Fire(x axis position,...)
    player = Player(110, HEIGHT - 50, 50, 50)
    fire = Fire(800, HEIGHT - block_size - 64, 15, 32)
    fire.on()
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH*2 // block_size, (WIDTH * 4) // block_size)]

    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size),
               Block(block_size * -10, HEIGHT - block_size * 2, block_size),
               Block(block_size * -10, HEIGHT - block_size * 3, block_size),
               Block(block_size * -10, HEIGHT - block_size * 4, block_size),
               Block(block_size * -10, HEIGHT - block_size * 5, block_size),
               Block(block_size * -10, HEIGHT - block_size * 6, block_size),
               Block(block_size * 4, HEIGHT - block_size * 2, block_size),
               Block(block_size * 5, HEIGHT - block_size * 3, block_size),
               Block(block_size * 5, HEIGHT - block_size * 2, block_size),
               Block(block_size * 9, HEIGHT - block_size * 2, block_size),
               Block(block_size * 10, HEIGHT - block_size * 2, block_size),
               Block(block_size * 20, HEIGHT - block_size * 3, block_size),
               Block(block_size * 21, HEIGHT - block_size * 3, block_size),
               Block(block_size * 22, HEIGHT - block_size * 3, block_size),
               Block(block_size * 39, HEIGHT - block_size * 2, block_size),
               Block(block_size * 40, HEIGHT - block_size * 1, block_size),
               Block(block_size * 40, HEIGHT - block_size * 2, block_size),
               Block(block_size * 40, HEIGHT - block_size * 3, block_size),
               Block(block_size * 41, HEIGHT - block_size * 1, block_size),
               Block(block_size * 41, HEIGHT - block_size * 2, block_size),
               Block(block_size * 41, HEIGHT - block_size * 3, block_size),
               Block(block_size * 41, HEIGHT - block_size * 4, block_size),
               Block(block_size * 41, HEIGHT - block_size * 5, block_size),
               Block(block_size * 41, HEIGHT - block_size * 6, block_size),
               fire,
               Fire(-830, HEIGHT - block_size - 64, 15, 32),
               Fire(2050, HEIGHT - block_size * 3 - 64, 15, 32),
               Fire(3775, HEIGHT - block_size * 2 - 64, 15, 32),
               ]

    offset_x = 0
    # how far off to side you go
    scroll_area_width = 300

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)
        fire.loop()
        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
