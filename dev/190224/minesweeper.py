import pygame
import random

# Define colours
colours = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (213, 50, 80),
}

# Initialise pygame
pygame.init()

# Set up window and display
width, height = 600, 400
game_display = pygame.display.set_mode((width, height))
playable_height = 320  # 320 is the height of the playable area
pygame.display.set_caption('Minesweeper Prototype')
font_style = pygame.font.SysFont(None, 35)


def readDNA():
    with open('snake_scores.csv', 'r') as dna:
        line = dna.readlines()[-1]
    return line


# Used to display text to the user
def showText(msg, color, x, y):
    msg = font_style.render(msg, True, color)
    game_display.blit(msg, [x, y])


# Load and draw the elements of the game ready for the player to begin
def initGame():
    # Generate grid with random squares selected as outliers
    for row in range(0, width, 40):
        for col in range(0, playable_height, 40):
            if not random.randint(0, 10) == 0:
                # The odd numbered squares give the user lines between the cells to distinguish them
                pygame.draw.rect(game_display, colours['white'], [row + 1, col + 1, 39, 39])
            else:
                pygame.draw.rect(game_display, colours['black'], [row + 1, col + 1, 39, 39])

    showText('Minesweeper', colours['white'], 0, 330)

    pygame.display.update()


def gameLoop():
    # Used to end the game
    game_over = False
    game_lost = False
    game_close = False

    while not game_over:
        # Handle user input for endgame
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_over = True
                    game_close = False
                if event.key == pygame.K_c:
                    gameLoop()


initGame()
gameLoop()
