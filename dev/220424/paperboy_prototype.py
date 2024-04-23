import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scrolling Background")

# Define colors and their rgb values
colours = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (213, 50, 80),
    'green': (0, 255, 0),
    'blue': (50, 153, 213),
    'yellow': (255, 255, 0)
}

# Load the background image
background = pygame.image.load("assets/test_background.jpg")
background_rect = background.get_rect()

# Set up the player
player = pygame.Rect(50, 50, 50, 50)
player_color = colours['red']
player_speed = 5

# The main game loop
def main():



# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the keys pressed
    keys = pygame.key.get_pressed()

    # Move the player
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
    if keys[pygame.K_UP]:
        player.y -= player_speed
    if keys[pygame.K_DOWN]:
        player.y += player_speed

    # Scrolling the background
    if player.right > WIDTH:
        background_rect.x -= player_speed
        player.x -= player_speed
    if player.left < 0:
        background_rect.x += player_speed
        player.x += player_speed
    if player.bottom > HEIGHT:
        background_rect.y -= player_speed
        player.y -= player_speed
    if player.top < 0:
        background_rect.y += player_speed
        player.y += player_speed

    # Fill the screen with white
    screen.fill(colours['white'])

    # Draw the background
    screen.blit(background, background_rect)

    # Draw the player
    pygame.draw.rect(screen, player_color, player)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

main()

# Quit Pygame
pygame.quit()
sys.exit()
