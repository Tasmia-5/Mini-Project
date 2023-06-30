import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Menu")

# Colors
WHITE = (255, 255, 255)
LIGHT_BLUE = (135, 206, 250)

# Fonts
font = pygame.font.Font(None, 36)

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

# Game variables
volume = 50
pin = ""

# Button actions
def start_action():
    print("Start")

def volume_increase_action():
    global volume
    volume += 10
    print("Volume Increased:", volume)

def volume_decrease_action():
    global volume
    volume -= 10
    print("Volume Decreased:", volume)

def unlock_action():
    global pin
    pin += "*"
    print("Unlocking... PIN:", pin)

# Create buttons
button_width = 200
button_height = 50
button_x = screen_width // 2 - button_width // 2

start_button = Button(button_x, 200, button_width, button_height, "Start / Try Again", LIGHT_BLUE, WHITE, start_action)
volume_increase_button = Button(button_x, 275, button_width, button_height, "Volume +", LIGHT_BLUE, WHITE, volume_increase_action)
volume_decrease_button = Button(button_x, 350, button_width, button_height, "Volume -", LIGHT_BLUE, WHITE, volume_decrease_action)
unlock_button = Button(button_x, 425, button_width, button_height, "Unlock", LIGHT_BLUE, WHITE, unlock_action)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        start_button.handle_event(event)
        volume_increase_button.handle_event(event)
        volume_decrease_button.handle_event(event)
        unlock_button.handle_event(event)

    # Clear the screen
    screen.fill(WHITE)

    # Draw the buttons
    start_button.draw(screen)
    volume_increase_button.draw(screen)
    volume_decrease_button.draw(screen)
    unlock_button.draw(screen)

    # Update the display
    pygame.display.flip()

pygame.quit()
