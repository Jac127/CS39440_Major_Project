import pygame
import time
import random

# Initialise PyGame
pygame.init()

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Set up window and display
width, height = 600, 400
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game Prototype')
font_style = pygame.font.SysFont(None, 35)

# Initialise game clock
clock = pygame.time.Clock()

# Snake properties
snake_block = 10
snake_speed = 15


# Draw the snake
def drawSnake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(game_display, black, [x[0], x[1], snake_block, snake_block])


# Used to display text to the user
def showText(msg, color):
    msg = font_style.render(msg, True, color)
    game_display.blit(msg, [width / 6, height / 3])


def gameLoop():
    # Used to end the game
    game_over = False
    game_close = False

    # Position the snake in the middle
    x1 = width / 2
    y1 = height / 2

    # Initialise the variables for change the snake's location
    x1_change = 0
    y1_change = 0

    # Initialise the snake variables
    snakeSegments = []
    snakeLength = 1

    # Randomly place food
    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    # Main game loop
    while not game_over:

        # Loops when the game has ended until the player responds
        while game_close:
            game_display.fill(white)
            showText("You lost! Press Q-Quit or C-Play Again", red)
            pygame.display.update()

            # Handle user input for endgame
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # Handle user input while playing game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Check if the snake collides with the outer walls
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        # Update the snake's position
        x1 += x1_change
        y1 += y1_change

        # Fill game background
        game_display.fill(white)

        # Draw food item
        pygame.draw.rect(game_display, green, [foodx, foody, snake_block, snake_block])

        # Update the snake and it's segments
        snakeHead = [x1, y1]
        snakeSegments.append(snakeHead)

        # Check the snake is the correct length
        if len(snakeSegments) > snakeLength:
            del snakeSegments[0]

        # Check if the snake collides with itself
        for x in snakeSegments[:-1]:
            if x == snakeHead:
                game_close = True

        # Draw the snake
        drawSnake(snake_block, snakeSegments)
        pygame.display.update()

        # Check if the food is eaten by the snake
        if x1 == foodx and y1 == foody:
            # Reposition the food
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            # Increase the length of the snake
            snakeLength += 1

        # Manage game speed
        clock.tick(snake_speed)

    # Handle quiting
    pygame.quit()
    quit()


gameLoop()