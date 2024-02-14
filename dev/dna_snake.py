import pygame
import time
import random

# Initialize PyGame
pygame.init()

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
yellow = (255, 255, 0)

# Set up window and display
width, height = 600, 400
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game Prototype')
font_style = pygame.font.SysFont(None, 35)

# Initialize game clock
clock = pygame.time.Clock()

# Snake properties
snake_block = 20
snake_speed = 10

# Define food colors and their effects on snake segments
food_colors = {
    'red': red,
    'green': green,
    'blue': blue,
    'yellow': yellow,
}
# Randomly choose a food color to start
current_food_color = random.choice(list(food_colors.values()))

# Draw the snake with segment-specific colors
def drawSnake(snake_block, snake_list, segment_colors):
    for i, segment in enumerate(snake_list):
        pygame.draw.rect(game_display, segment_colors[i], [segment[0], segment[1], snake_block, snake_block])

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

    # Initialize the variables for changing the snake's location
    x1_change = 0
    y1_change = 0

    # Initialize the snake variables
    snake_segments = []
    segment_colors = [black]  # Starting color of the snake
    snake_length = 1

    # Randomly place food
    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
    current_food_color = random.choice(list(food_colors.values()))

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

        x1 += x1_change
        y1 += y1_change
        game_display.fill(white)

        # Draw food item with the current color
        pygame.draw.rect(game_display, current_food_color, [foodx, foody, snake_block, snake_block])

        snake_head = [x1, y1]
        snake_segments.append(snake_head)
        if len(snake_segments) > snake_length:
            del snake_segments[0]

        # Ensure segment_colors matches the length of snake_segments
        if len(segment_colors) < len(snake_segments):
            segment_colors.append(current_food_color)

        # Check if the snake collides with itself
        for x in snake_segments[:-1]:
            if x == snake_head:
                game_close = True

        drawSnake(snake_block, snake_segments, segment_colors)
        pygame.display.update()

        # Check if the food is eaten by the snake
        if x1 < foodx + snake_block and x1 + snake_block > foodx and y1 < foody + snake_block and y1 + snake_block > foody:
            # Reposition the food
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            snake_length += 1
            # Add the current food color to the new segment
            segment_colors.append(current_food_color)
            current_food_color = random.choice(list(food_colors.values()))  # Select new food color

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
