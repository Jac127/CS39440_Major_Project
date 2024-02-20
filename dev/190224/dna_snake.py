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


# Detect collisions
def check_collision(x1, y1, x2, y2, block_size):
    # Calculate the center points of the snake's head and the food item
    center_x1 = x1 + block_size / 2
    center_y1 = y1 + block_size / 2
    center_x2 = x2 + block_size / 2
    center_y2 = y2 + block_size / 2

    # Calculate the distance between the centers
    distance = ((center_x2 - center_x1) ** 2 + (center_y2 - center_y1) ** 2) ** 0.5

    # If the distance is less than the size of a block, a collision is detected
    return distance < block_size


# Checks if nucleotides are matching pairs or if a new matching pair is possible
def checkNucleotideString(segments):
    no_segments = len(segments)

    # If all pairs are complete
    if no_segments % 2 == 0:
        slicedString = segments[-2:]

        if no_segments > 2:  # Prevents a warning being thrown at the start of the game before the sequence reaches a valuable length
            if 'AT' in slicedString:
                return
            elif 'TA' in slicedString:
                return
            elif 'GC' in slicedString:
                return
            elif 'CG' in slicedString:
                return
            else:
                print('Invalid nucleotide')


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

    # Randomly place food items
    food_one_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    food_one_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
    food_one_nucleotide = 'T'
    food_one_colour = colours.get(nucleotide_colours[food_one_nucleotide])

    food_two_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    food_two_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
    food_two_nucleotide = random.choice(list(nucleotide_colours.keys()))
    food_two_colour = colours.get(nucleotide_colours[food_two_nucleotide])

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
        pygame.draw.rect(game_display, food_one_colour, [food_one_x, food_one_y, snake_block, snake_block])
        showText(food_one_nucleotide, getColour('black'), food_one_x, food_one_y)
        pygame.draw.rect(game_display, food_two_colour, [food_two_x, food_two_y, snake_block, snake_block])
        showText(food_two_nucleotide, getColour('black'), food_two_x, food_two_y)

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
        if check_collision(x1, y1, food_one_x, food_one_y, snake_block) or check_collision(x1, y1, food_two_x, food_two_y, snake_block):
            # Add food that has been eaten to the snake, the if statement ensure it's the correct one
            if x1 < food_one_x + snake_block and x1 + snake_block > food_one_x and y1 < food_one_y + snake_block:
                # Add the current food color to the new segment
                segment_nucleotides += food_one_nucleotide
            else:
                # Add the current food color to the new segment
                segment_nucleotides += food_two_nucleotide

            # Reposition the food
            food_one_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            food_one_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            food_two_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            food_two_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            snake_length += 1

            # Assign nucleotides to food, based on the last characters eaten
            last_two_chars = segment_nucleotides[-2:]

            if 'AT' in last_two_chars:
                food_one_nucleotide = random.choice(list(nucleotide_colours))
                food_one_colour = colours.get(nucleotide_colours[food_one_nucleotide])
            elif 'TA' in last_two_chars:
                food_one_nucleotide = random.choice(list(nucleotide_colours))
                food_one_colour = colours.get(nucleotide_colours[food_one_nucleotide])
            elif 'GC' in last_two_chars:
                food_one_nucleotide = random.choice(list(nucleotide_colours))
                food_one_colour = colours.get(nucleotide_colours[food_one_nucleotide])
            elif 'CG' in last_two_chars:
                food_one_nucleotide = random.choice(list(nucleotide_colours))
                food_one_colour = colours.get(nucleotide_colours[food_one_nucleotide])
            else:
                last_char = last_two_chars[1]

                # Set food nucleotide to matching pair
                if last_char == 'A':
                    food_one_nucleotide = 'T'
                    food_one_colour = colours.get(nucleotide_colours[food_one_nucleotide])
                elif last_char == 'T':
                    food_one_nucleotide = 'A'
                    food_one_colour = colours.get(nucleotide_colours[food_one_nucleotide])
                elif last_char == 'G':
                    food_one_nucleotide = 'C'
                    food_one_colour = colours.get(nucleotide_colours[food_one_nucleotide])
                elif last_char == 'C':
                    food_one_nucleotide = 'G'
                    food_one_colour = colours.get(nucleotide_colours[food_one_nucleotide])

            checkNucleotideString(segment_nucleotides)

        clock.tick(snake_speed)

    pygame.quit()
    print(segment_nucleotides)
    quit()


gameLoop()
