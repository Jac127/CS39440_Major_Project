import math

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
font_style = pygame.font.SysFont(None, 27)


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
                new_list.append(strings[line_counter][:-1])  # The slice index removes the newline char
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


# Calculate which tile the mouse is currently on
def calculateTile(mouse_Pos):
    x = mouse_Pos[0]
    y = mouse_Pos[1]

    tileX = math.floor(x / 150)
    tileY = math.floor(y / 150)

    return tileX, tileY


def moveTiles(direction, tiles):
    # Initialise empty tile coordinates
    empty_TileX = 0
    empty_TileY = 0

    # Find empty tile coords
    for x in range(0, 4):
        for y in range(0, 4):
            if tiles[x][y] == '':
                empty_TileX = x
                empty_TileY = y

    # Move tiles to fill empty space
    if direction == 'up':
        while empty_TileY < 3:
            tiles[empty_TileX][empty_TileY] = tiles[empty_TileX][empty_TileY + 1]
            empty_TileY = empty_TileY + 1
            tiles[empty_TileX][empty_TileY] = ''

    if direction == 'down':
        while empty_TileY > 0:
            tiles[empty_TileX][empty_TileY] = tiles[empty_TileX][empty_TileY - 1]
            empty_TileY -= 1
            tiles[empty_TileX][empty_TileY] = ''

    if direction == 'left':
        while empty_TileX < 3:
            tiles[empty_TileX][empty_TileY] = tiles[empty_TileX + 1][empty_TileY]
            empty_TileX += 1
            tiles[empty_TileX][empty_TileY] = ''

    if direction == 'right':
        while empty_TileX > 0:
            tiles[empty_TileX][empty_TileY] = tiles[empty_TileX - 1][empty_TileY]
            empty_TileX -= 1
            tiles[empty_TileX][empty_TileY] = ''

    return tiles


# Preparations before game loop begins
def initGame():
    tiles = readDNA()

    game_display.fill(colours['white'])
    pygame.draw.line(game_display, colours['black'], (0, 600), (600, 600))  # Separates UI from game

    drawTiles(tiles)

    showText('Click on a tile to continue!', colours['black'], 5, 605)
    pygame.display.update()

    # Wait for tile click from user
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                tile_Pos = calculateTile(pygame.mouse.get_pos())  # Get specific tile index
                tile = tiles[tile_Pos[0]][tile_Pos[1]]  # Save DNA in tile
                tiles[tile_Pos[0]][tile_Pos[1]] = ''  # Set empty

                # Update ready for the player to continue
                drawTiles(tiles)
                showText('Selected sequence: ' + tile, colours['black'], 5, 630)

                pygame.display.update()

                waiting = False

    return tiles


def gameLoop(tiles):
    tiles = tiles
    # Used to end the game
    game_over = False
    game_lost = False
    game_close = False

    while not game_over:
        # Handle user input
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Quit the game
                    game_over = True
                if event.key == pygame.K_UP:
                    tiles = moveTiles('up', tiles)
                if event.key == pygame.K_DOWN:
                    tiles = moveTiles('down', tiles)
                if event.key == pygame.K_LEFT:
                    tiles = moveTiles('left', tiles)
                if event.key == pygame.K_RIGHT:
                    tiles = moveTiles('right', tiles)

        drawTiles(tiles)
        pygame.display.update()

    pygame.quit()
    quit()


gameLoop(initGame())
