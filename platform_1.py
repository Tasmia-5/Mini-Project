# -*- coding: utf-8 -*-
import pygame
import random
import math
import sys
import os
from os import listdir
from os.path import isfile, join
from pygame.mixer import*
from pygame.locals import QUIT

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
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('sounds/FiftyFifty_Cupid.mp3')
    music.play(-1)
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    SPRITES = load_sprite_sheets("Characters", "Frog", 32, 32, True)
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
    for obj in objects:
        if isinstance(obj, Fire) and collide_rect(player, obj):
            if obj.rect.x == -830:
                player.make_hit()
                display_picture("assets/picture.png")
            if obj.rect.x == 3775:
                player.make_hit()
                display_message("guess what...\nHappy Birthday!\nBut there is more...\nFind the mystery chest!", clock)


def display_picture(image_path):
    # Load the image
    image = pygame.image.load(image_path)

    # Create a new window to display the image
    picture_window = pygame.display.set_mode((image.get_width(), image.get_height()))

    # Display the image in the window
    picture_window.blit(image, (0, 0))
    pygame.display.flip()

    # Wait for the window to be closed
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()


def display_message(message, clock):
    pygame.init()
    pygame.mixer.init()
    # pygame.mixer.music.load('sounds/Fireworks_pewpew.mp3')
    pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds/Happy_Bday.mp3'))
    pygame.mixer.Channel(2).play(pygame.mixer.Sound('sounds/Fireworks_pewpew.mp3'))
    music.play(0)
    # Create a new window to display the message
    message_window = pygame.display.set_mode((WIDTH, HEIGHT))

    # Set the window title
    pygame.display.set_caption("Special Message")

    restart_button_rect = pygame.Rect(WIDTH // 3, HEIGHT - 75, 250, 60)
    # Render the message text
    # fonts: Nicotine.ttf , Jedisf3Dital.ttf, Alien Mushrooms.otf, Minecraft.ttf, YourStarTtf.ttf, nyetlaserital.otf
    font = pygame.font.Font('Jedisf3Dital.ttf', 32)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    return True

        message_window.fill((229, 182, 247))  # Fill the window with lilac color

        for i, message in enumerate(message):
            # Convert the message to Unicode string
            text = font.render("GUESS WHAT!! It's your Birthday!!!", 0, (0, 0, 0))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 420))
            message_window.blit(text, text_rect)

            text2 = font.render(": ! ! : ! . . : . ! . ! : ! : . Happy Birthday . : ! : ! . ! . : . . ! : ! ! :", 0, (0, 0, 0))
            text2_rect = text2.get_rect(center=(WIDTH // 2, HEIGHT - 300))
            message_window.blit(text2, text2_rect)

            text3 = font.render("Here is a challenge, find the mystery chest", 0, (0, 0, 0))
            text3_rect = text3.get_rect(center=(WIDTH // 2, HEIGHT - 180))
            message_window.blit(text3, text3_rect)

            text4 = font.render("(  Hint: Play again  )", 0, (0, 0, 0))
            text4_rect = text4.get_rect(center=(WIDTH // 2, HEIGHT - 100))
            message_window.blit(text4, text4_rect)

        # Rest of the code...

        pygame.display.update()

        clock.tick(FPS)


def replay_button():
    pass


def collide_rect(sprite1, sprite2):
    return sprite1.rect.colliderect(sprite2.rect)


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    block_size = 96
    # Player(x axis posit...)
    # (...- block_size - "height", range of animation/sprite, bottom of object range)
    # Fire(x axis position,...)
    player = Player(210, HEIGHT - 50, 50, 50)
    fire = Fire(-530, HEIGHT - block_size - 64, 15, 32)
    fire.on()
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH*2 // block_size, (WIDTH * 4) // block_size)]
    # where the floor, grass blocks, and fire you want to place them
    objects = [*floor,
               fire,
               Fire(800, HEIGHT - block_size - 64, 15, 32),
               Fire(2050, HEIGHT - block_size * 3 - 64, 15, 32),
               Fire(3775, HEIGHT - block_size * 2 - 64, 15, 32),
               Block(block_size * -10, HEIGHT - block_size * 2, block_size),
               Block(block_size * -10, HEIGHT - block_size * 3, block_size),
               Block(block_size * -10, HEIGHT - block_size * 4, block_size),
               Block(block_size * -10, HEIGHT - block_size * 5, block_size),
               Block(block_size * -10, HEIGHT - block_size * 6, block_size),
               Block(block_size * 5, HEIGHT - block_size * 2, block_size),
               Block(block_size * 6, HEIGHT - block_size * 3, block_size),
               Block(block_size * 6, HEIGHT - block_size * 2, block_size),
               Block(block_size * 10, HEIGHT - block_size * 2, block_size),
               Block(block_size * 11, HEIGHT - block_size * 2, block_size),
               Block(block_size * 19, HEIGHT - block_size * 3, block_size),
               Block(block_size * 20, HEIGHT - block_size * 3, block_size),
               Block(block_size * 21, HEIGHT - block_size * 3, block_size),
               Block(block_size * 22, HEIGHT - block_size * 3, block_size),
               Block(block_size * 23, HEIGHT - block_size * 3, block_size),
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

               ]

    offset_x = 0
    # how far off to side you go
    scroll_area_width = 400

    goofy_pic1 = pygame.image.load("assets/goofy_pic1.png")
    player_colliding = False
    message_window = pygame.display.set_mode((WIDTH, HEIGHT))
    message_start_time = 0

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

        if player.rect.colliderect(fire.rect):
            # Show the message and set the flag to True
            if not player_colliding:
                player_colliding = True
                message_start_time = pygame.time.get_ticks()
                message_window.blit(goofy_pic1, goofy_pic1.get_rect(center=(200, 20)))

            # Check if the message should stay on screen for 3 seconds
        if player_colliding and pygame.time.get_ticks() - message_start_time >= 10000:
            player_colliding = False

        player.loop(FPS)
        fire.loop()
        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

        if player_colliding:
            message_window.blit(goofy_pic1, (0, 0))
            pygame.display.update()

    pygame.quit()
    quit()


if __name__ == "__main__":
    clock = pygame.time.Clock()
    main(window)
