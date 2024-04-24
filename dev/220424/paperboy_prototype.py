import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 800, 600
game_display = pygame.display.set_mode((width, height))
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
background = pygame.image.load("assets/background.jpg")
background_rect = background.get_rect()

# Set up the player
player = pygame.Rect(50, 50, 50, 50)
player_color = colours['red']
player_speed = 5


def main():
    # Used to end the game
    game_over = False
    game_lost = False
    game_close = False
    saved = False

    # Main game loop
    while not game_over:
        # Loops when the game has ended until the player responds
        while game_close:
            game_display.fill(colours['white'])

            # Handle user input for endgame
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        main()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get the keys pressed
        keys = pygame.key.get_pressed()

        # Move the player
        if keys[pygame.K_LEFT] and background_rect.x <= -5:
            player.x -= player_speed
            background_rect.x += 5

        if keys[pygame.K_RIGHT] and background_rect.x >= -4665:
            player.x += player_speed
            background_rect.x -= 5

        if keys[pygame.K_UP] and background_rect.y <= -5:
            player.y -= player_speed
            background_rect.y += 5

        if keys[pygame.K_DOWN] and -3035 <= background_rect.y:
            player.y += player_speed
            background_rect.y -= 5

        # Scrolling the background
        if player.right > width:
            background_rect.x -= player_speed
            player.x -= player_speed
        if player.left < 0:
            background_rect.x += player_speed
            player.x += player_speed
        if player.bottom > height:
            background_rect.y -= player_speed
            player.y -= player_speed
        if player.top < 0:
            background_rect.y += player_speed
            player.y += player_speed

        # Fill the screen with white
        game_display.fill(colours['white'])

        # Draw the background
        game_display.blit(background, background_rect)

        # Draw the player
        pygame.draw.rect(game_display, player_color, player)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        pygame.time.Clock().tick(60)


main()

# Quit Pygame
pygame.quit()
sys.exit()
