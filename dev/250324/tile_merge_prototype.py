import math
import time

import pygame
import random

# Define colours
colours = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (213, 50, 80),
}

# Initialise the global dna strings list
strings = []

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
    with open('snake_scores.csv', 'r') as dna:
        for line in dna:
            strings.append(line[:12])

    # Create 2d list with values from previous list
    tiles = []
    line_counter = 0
    for i in range(0, 4):
        new_list = []
        for j in range(0, 4):
            if line_counter < len(strings):
                # The slice index is temporary, should be set to -1 in final project to remove newline char
                new_list.append(strings[line_counter])
            else:  # If there is not enough sequences make duplicates
                new_list.append(random.choice(strings))

            line_counter += 1
        tiles.append(new_list)

    return tiles


# Used to display text to the user
def showText(msg, color, x, y):
    msg = font_style.render(msg, True, color)
    game_display.blit(msg, [x, y])


# Draw the tiles
def drawTiles(tiles):
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

                # Write the sequence contained on the tile
                showText(tiles[i][j], colours['white'], row, col + 75)
            else:
                pygame.draw.rect(game_display, colours['white'], [row + 1, col + 1, 149, 149])

    pygame.display.update()


# Calculate which tile the mouse is currently on
def calculateTile(mouse_Pos):
    x = mouse_Pos[0]
    y = mouse_Pos[1]

    tileX = math.floor(x / 150)
    tileY = math.floor(y / 150)

    return tileX, tileY


# Used in merging, if there is an overlap, the strings will be compatible for merging
def hasOverlap(tile1, tile2):
    for i in range(len(tile1) - 2):  # Iterate through each three-character sequence in tile1
        sequence = tile1[i:i + 3]
        if sequence in tile2:  # Check if the three-character sequence exists in tile2
            return True

    for i in range(len(tile2) - 2):  # Iterate through each three-character sequence in tile2
        sequence = tile2[i:i + 3]
        if sequence in tile1:  # Check if the three-character sequence exists in tile1
            return True

    return False


# Merges the DNA strings at the overlap
def mergeStrings(tile1, tile2):
    overlap = 3

    # Find the index where the overlap occurs
    overlapIndex = 0
    for i in range(len(tile1) - overlap + 1):
        if tile2.startswith(tile1[i:]):
            overlapIndex = i
            break

    # Merge the strings at the overlap
    mergedString = tile1[:overlapIndex] + tile2

    return mergedString


# Moves the tiles based on the direction
def moveTiles(direction, tiles):
    # Create a list of non-empty tiles
    fullTiles = [(i, j) for i in range(0, 4) for j in range(0, 4) if tiles[i][j] != '']

    # Move every tile
    for i in range(0, 4):
        for j in range(0, 4):
            # If the tile is not empty
            if (i, j) in fullTiles:
                # Save its details
                currentTile = tiles[i][j]
                tileX = i
                tileY = j

                if direction == 'up':
                    while tileY > 0:
                        if tiles[tileX][tileY - 1] == '':  # If the tile above is empty, move the tiles up
                            tiles[tileX][tileY - 1] = currentTile
                            tiles[tileX][tileY] = ''
                            tileY -= 1
                        elif hasOverlap(tiles[tileX][tileY - 1], tiles[tileX][tileY]):  # If the tiles have overlap
                            mergedTile = mergeStrings(tiles[tileX][tileY - 1], tiles[tileX][tileY])
                            tiles[tileX][tileY - 1] = mergedTile
                            tiles[tileX][tileY] = ''

                            if tiles[tileX][tileY - 1] == '':  # If the tile above is empty, move the tiles up
                                tiles[tileX][tileY - 1] = currentTile
                                tiles[tileX][tileY] = ''
                                tileY -= 1
                        else:
                            tileY = 0

                if direction == 'down':
                    while tileY < 3:
                        if tiles[tileX][tileY + 1] == '':
                            tiles[tileX][tileY + 1] = currentTile
                            tiles[tileX][tileY] = ''
                            tileY += 1
                        elif hasOverlap(tiles[tileX][tileY + 1], tiles[tileX][tileY]):  # If the tiles have overlap
                            mergedTile = mergeStrings(tiles[tileX][tileY + 1], tiles[tileX][tileY])
                            tiles[tileX][tileY + 1] = mergedTile
                            tiles[tileX][tileY] = ''

                            if tiles[tileX][tileY + 1] == '':
                                tiles[tileX][tileY + 1] = currentTile
                                tiles[tileX][tileY] = ''
                                tileY += 1
                        else:
                            tileY = 3

                if direction == 'left':
                    while tileX > 0:
                        if tiles[tileX - 1][tileY] == '':
                            tiles[tileX - 1][tileY] = currentTile
                            tiles[tileX][tileY] = ''
                            tileX -= 1
                        elif hasOverlap(tiles[tileX - 1][tileY], tiles[tileX][tileY]):  # If the tiles have overlap
                            mergedTile = mergeStrings(tiles[tileX - 1][tileY], tiles[tileX][tileY])
                            tiles[tileX - 1][tileY] = mergedTile
                            tiles[tileX][tileY] = ''

                            if tiles[tileX - 1][tileY] == '':
                                tiles[tileX - 1][tileY] = currentTile
                                tiles[tileX][tileY] = ''
                                tileX -= 1
                        else:
                            tileX = 0

                if direction == 'right':
                    while tileX < 3:
                        if tiles[tileX + 1][tileY] == '':
                            tiles[tileX + 1][tileY] = currentTile
                            tiles[tileX][tileY] = ''
                            tileX += 1
                        elif hasOverlap(tiles[tileX + 1][tileY], tiles[tileX][tileY]):  # If the tiles have overlap
                            mergedTile = mergeStrings(tiles[tileX + 1][tileY], tiles[tileX][tileY])
                            tiles[tileX + 1][tileY] = mergedTile
                            tiles[tileX][tileY] = ''

                            if tiles[tileX + 1][tileY] == '':
                                tiles[tileX + 1][tileY] = currentTile
                                tiles[tileX][tileY] = ''
                                tileX += 1
                        else:
                            tileX = 3

    return tiles


# Adds a new tile to a random empty space
def newTile(tiles):
    # Create a list of empty tiles
    emptyTiles = [(i, j) for i in range(0, 4) for j in range(0, 4) if tiles[i][j] == '']

    i, j = random.choice(emptyTiles)  # Choose a random empty space
    tiles[i][j] = random.choice(strings)  # Choose a random string

    return tiles


# Preparations before game loop begins
def initGame():
    tiles = readDNA()
    tile_pos = 0, 0

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
                tile_pos = calculateTile(pygame.mouse.get_pos())  # Get specific tile index
                tile = tiles[tile_pos[0]][tile_pos[1]]  # Save DNA in tile

                # Update ready for the player to continue
                drawTiles(tiles)
                showText('Selected sequence: ' + tile, colours['black'], 5, 630)

                pygame.display.update()

                waiting = False

    # Move selected tile to top right
    selected_tile = tiles[tile_pos[0]][tile_pos[1]]  # Save selected tile
    strings.remove(selected_tile)  # Removes string in play from list

    # Clear all tiles
    for row in range(0, 4):
        for tile in range(0, 4):
            tiles[row][tile] = ''

    tiles[0][0] = selected_tile  # Set top right to selected tile

    time.sleep(0.5)
    newTile(tiles)

    return tiles


# The function that is called every move
def nextMove(tiles):
    tiles = newTile(tiles)

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

                tiles = nextMove(tiles)

                if tiles is False:  # Loss condition
                    game_lost = True

                gameLoop(tiles)

        # Loss condition
        if len([(i, j) for i in range(0, 4) for j in range(0, 4) if tiles[i][j] == '']) == 0:
            game_lost = True
            game_over = True

        drawTiles(tiles)
        pygame.display.update()

    pygame.quit()
    quit()


gameLoop(initGame())
