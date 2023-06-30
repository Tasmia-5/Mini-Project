import pygame
import sys
from pygame.locals import QUIT

# Initialize pygame
pygame.init()

# Set the window dimensions
WIDTH = 1000
HEIGHT = 500

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Define fonts
font = pygame.font.SysFont("arialblack", 40)

# Define colors
TEXT_COL = (255, 255, 255)
BUTTON_COL = (137, 207, 240)
BUTTON_HOVER_COL = (165, 220, 240)

# Define button dimensions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_SPACING = 20

# Define menu state
menu_state = "main"

# Function to handle the main menu
def main_menu():
    while True:
        # Clear the screen
        window.fill((0, 0, 0))

        # Draw the menu buttons and text
        draw_menu_buttons()

        pygame.display.update()

        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a button is clicked
                mouse_pos = pygame.mouse.get_pos()
                if is_button_clicked(mouse_pos, 1):
                    # Start the game
                    game_loop()

# Function to draw the menu buttons and text
def draw_menu_buttons():
    button_font = pygame.font.Font(None, 50)
    duck_text = button_font.render("DUCK", True, TEXT_COL)
    frog_text = button_font.render("FROG", True, TEXT_COL)

    # Calculate button positions
    button_x = WIDTH // 2 - BUTTON_WIDTH // 2
    duck_button_y = HEIGHT // 2 - BUTTON_HEIGHT // 2
    frog_button_y = duck_button_y + BUTTON_HEIGHT + BUTTON_SPACING

    # Draw the buttons
    pygame.draw.rect(window, BUTTON_COL, (button_x, duck_button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(window, BUTTON_COL, (button_x, frog_button_y, BUTTON_WIDTH, BUTTON_HEIGHT))

    # Draw the text on buttons
    duck_text_rect = duck_text.get_rect(center=(WIDTH // 2, duck_button_y + BUTTON_HEIGHT // 2))
    frog_text_rect = frog_text.get_rect(center=(WIDTH // 2, frog_button_y + BUTTON_HEIGHT // 2))
    window.blit(duck_text, duck_text_rect)
    window.blit(frog_text, frog_text_rect)

# Function to check if a button is clicked
def is_button_clicked(mouse_pos, button_number):
    button_x = WIDTH // 2 - BUTTON_WIDTH // 2
    button_y = HEIGHT // 2 - BUTTON_HEIGHT // 2 + (button_number - 1) * (BUTTON_HEIGHT + BUTTON_SPACING)
    button_rect = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
    return button_rect.collidepoint(mouse_pos)

# Function to handle the game loop
def game_loop():
    # Your game logic goes here
    pass

# Start the game by calling the main menu
main_menu()
