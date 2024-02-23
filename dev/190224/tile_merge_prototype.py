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
width, height = 600, 680
game_display = pygame.display.set_mode((width, height))
playable_height = 600  # 600 is the height of the playable area
pygame.display.set_caption('Tile Merge Prototype')
font_style = pygame.font.SysFont(None, 35)


# Read in each DNA string to a format that represents a grid of tiles
def readDNA():
    # Put DNA data into a list
    strings = []
    with open('snake_scores.csv', 'r') as dna:
        for line in dna:
            strings.append(line)

    # Create 2d list with values from previous list
    tiles = []
    line_counter = 0
    for i in range(0, 4):
        new_list = []
        for j in range(0, 4):
            if line_counter < len(strings):
                new_list.append(strings[line_counter])
            else:  # If there is not enough sequences make duplicates
                new_list.append(random.choice(strings))

            line_counter += 1
        tiles.append(new_list)

    return tiles


# Draw the tiles
def drawTiles(tiles):
    current_tile = 0

    # Draw grid. The block size for the grid is 150px
    for row in range(0, width, 150):
        for col in range(0, playable_height, 150):
            # Convert px to index for tile matching
            i = int(row / 150)
            j = int(col / 150)

            # The empty tiles appear as white
            if tiles[i][j] != '':
                # The odd numbered value give the user lines between the cells to distinguish them
                pygame.draw.rect(game_display, colours['black'], [row + 1, col + 1, 149, 149])
            else:
                pygame.draw.rect(game_display, colours['white'], [row + 1, col + 1, 149, 149])

            current_tile += 1
    pygame.display.update()


# Used to display text to the user
def showText(msg, color, x, y):
    msg = font_style.render(msg, True, color)
    game_display.blit(msg, [x, y])


# Preparations before game loop begins
def initGame():
    tiles = readDNA()

    game_display.fill(colours['white'])
    pygame.draw.line(game_display, colours['black'], (0, 600), (600, 600))  # Separates UI from game

    drawTiles(tiles)

    showText('Click on a tile to continue!', colours['black'], 5, 605)
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