import pygame
import time
import random

# Initialize PyGame
pygame.init()

# Set up window and display
width, height = 600, 400
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game Prototype')
font_style = pygame.font.SysFont(None, 35)

# Initialize game clock
clock = pygame.time.Clock()

# Snake properties
snake_block = 20
snake_speed = 15

# Define food colors and their effects on snake segments
colours = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (213, 50, 80),
    'green': (0, 255, 0),
    'blue': (50, 153, 213),
    'yellow': (255, 255, 0)
}

# Define which food colour corresponds to the DNA nucleotides
nucleotide_colours = {
    'A': 'red',
    'T': 'green',
    'G': 'blue',
    'C': 'yellow'
}

# Define matching pairs
nucleotide_pairs = {
    'A': 'T',
    'T': 'A',
    'G': 'C',
    'C': 'G'
}

# Define list to hold boolean values that signify if a nucleotide in the string is valid
correct_segments = []

# Randomly choose a food colour to start
current_food_color = random.choice(list(nucleotide_colours))


# Used to display text to the user
def showText(msg, color, x, y):
    msg = font_style.render(msg, True, color)
    game_display.blit(msg, [x, y])


# Retrieves colour from dictionary
def getColour(colour):
    return colours[colour]


# Checks if nucleotides are matching pairs or if a new matching pair is possible
def checkNucleotideString(segments):
    no_segments = len(segments)
    slicedString = segments[-3:]

    if no_segments > 2: # Prevents a warning being thrown at the start of the game before the sequence reaches a valuable length
        if 'AT' in slicedString:
            return True
        elif 'TA' in slicedString:
            return True
        elif 'GC' in slicedString:
            return True
        elif 'CG' in slicedString:
            return True
        else:
            print('Invalid nucleotide')
            return False


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
    segment_nucleotides = 'A'  # Starting nucleotide of the snake
    snake_length = 1

    # Randomly place food
    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
    food_nucleotide = random.choice(list(nucleotide_colours))
    food_colour = colours.get(nucleotide_colours[food_nucleotide])

    # Main game loop
    while not game_over:

        # Loops when the game has ended until the player responds
        while game_close:
            game_display.fill(getColour('white'))
            showText("You lost! Press Q-Quit or C-Play Again", getColour('red'), width / 6, height / 3)
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
        game_display.fill(getColour('white'))

        # Draw food item with the current color and nucleotide character
        pygame.draw.rect(game_display, food_colour, [foodx, foody, snake_block, snake_block])
        showText(food_nucleotide, getColour('black'), foodx, foody)

        snake_head = [x1, y1]
        snake_segments.append(snake_head)
        if len(snake_segments) > snake_length:
            del snake_segments[0]

        # Check if the snake collides with itself
        for x in snake_segments[:-1]:
            if x == snake_head:
                game_close = True

        # Draw the snake with segment-specific colors and DNA nucleotides
        for i, segment in enumerate(snake_segments):
            pygame.draw.rect(game_display, getColour(nucleotide_colours[segment_nucleotides[i]]),
                             [segment[0], segment[1], snake_block, snake_block])
            showText(segment_nucleotides[i], getColour('black'), segment[0], segment[1])

        pygame.display.update()

        # Check if the food is eaten by the snake
        if x1 < foodx + snake_block and x1 + snake_block > foodx and y1 < foody + snake_block and y1 + snake_block > foody:
            # Reposition the food
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            snake_length += 1
            # Add the current food color to the new segment
            segment_nucleotides += food_nucleotide

            # Select new food colour and nucleotide
            food_nucleotide = random.choice(list(nucleotide_colours))
            food_colour = colours.get(nucleotide_colours[food_nucleotide])

            checkNucleotideString(segment_nucleotides)

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
