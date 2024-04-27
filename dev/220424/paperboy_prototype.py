import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 1500, 750
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Scrolling Background")
# Cap the frame rate
pygame.time.Clock().tick(60)

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
background = pygame.image.load("assets/background.jpg").convert()
background_rect = background.get_rect()

# Set up the player
# Takes image generated from character selection
playerImg = pygame.image.load("assets/generatedCharacter.png").convert_alpha()
player = pygame.Rect(370, 0, 20, 20)
player_speed = 5

# Define the valid movement areas or paths
roads = [
    pygame.Rect(380, 20, 1, 140),
    pygame.Rect(30, 160, 1350, 1),
    pygame.Rect(30, 160, 1, 612),
    pygame.Rect(315, 160, 1, 337),
    pygame.Rect(30, 317, 285, 1),
    pygame.Rect(30, 473, 285, 1),
    pygame.Rect(30, 630, 426, 1),
    pygame.Rect(315, 497, 140, 1),
    pygame.Rect(455, 335, 1, 310),
    pygame.Rect(455, 335, 490, 1),
    pygame.Rect(945, 335, 1, 310),
    pygame.Rect(455, 645, 490, 1),
    pygame.Rect(1245, 160, 1, 638),
    pygame.Rect(1380, 160, 1, 638),
    pygame.Rect(1380, 225, 105, 1),
    pygame.Rect(1245, 325, 245, 1),
    pygame.Rect(1245, 427, 245, 1),
    pygame.Rect(1245, 530, 245, 1),
    pygame.Rect(1245, 635, 245, 1),
    pygame.Rect(1245, 737, 245, 1)]


# Main game function
def main():
    # Used to end the game
    game_over = False

    # Main game loop
    while not game_over:
        # Will be used for ending the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Get the keys pressed
        keys = pygame.key.get_pressed()

        # Move the player if the movement is within valid areas
        if keys[pygame.K_LEFT]:
            player.move_ip(-player_speed, 0)
            for area in roads:
                if player.colliderect(area):
                    break
            else:
                player.move_ip(player_speed, 0)

        if keys[pygame.K_RIGHT]:
            player.move_ip(player_speed, 0)
            for area in roads:
                if player.colliderect(area):
                    break
            else:
                player.move_ip(-player_speed, 0)

        if keys[pygame.K_UP]:
            player.move_ip(0, -player_speed)
            for area in roads:
                if player.colliderect(area):
                    break
            else:
                player.move_ip(0, player_speed)

        if keys[pygame.K_DOWN]:
            player.move_ip(0, player_speed)
            for area in roads:
                if player.colliderect(area):
                    break
            else:
                player.move_ip(0, -player_speed)

        # Fill the screen with white
        game_display.fill(colours['white'])

        # Draw the background
        game_display.blit(background, background_rect)

        # Draw road lines, used to see where you can move and for aesthetics
        for line in roads:
            pygame.draw.rect(game_display, colours['white'], line)

        # Draw the player
        game_display.blit(playerImg, player)

        # Update the display
        pygame.display.flip()


main()

# Quit Pygame
pygame.quit()
