import pygame
import csv
import random

# Define colors and their rgb values
colours = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (213, 50, 80),
    'green': (0, 255, 0),
    'blue': (50, 153, 213),
    'yellow': (255, 255, 0)
}

# Initialize PyGame
pygame.init()

# Set up window and display
width, height = 600, 400
game_display = pygame.display.set_mode((width, height))
playable_height = 320  # 320 is the height of the playable area
pygame.display.set_caption('Snake Game Prototype')
font_style = pygame.font.SysFont(None, 35)

# Initialize game clock
clock = pygame.time.Clock()

# Game object properties
block_size = 20
snake_speed = 15

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


# Used to display text to the user
def showText(msg, color, x, y):
    msg = font_style.render(msg, True, color)
    game_display.blit(msg, [x, y])


# Detect collisions between blocks
def block_collision(x1, y1, x2, y2, block_size):
    # Calculate the center points of the snake's head and the food item
    center_x1 = x1 + block_size / 2
    center_y1 = y1 + block_size / 2
    center_x2 = x2 + block_size / 2
    center_y2 = y2 + block_size / 2

    # Calculate the distance between the centers
    distance = ((center_x2 - center_x1) ** 2 + (center_y2 - center_y1) ** 2) ** 0.5

    # If the distance is less than the size of a block, a collision is detected
    return distance < block_size


# Returns an array that represents validity of each nucleotide in the sequence
def checkNucleotideString(segments):
    no_segments = len(segments)
    valid_segments = []

    for i in range(0, no_segments, 2):
        if i + 1 < no_segments:  # Ensure there is a pair to check
            pair = segments[i:i+2]
            if pair in ['AT', 'TA', 'GC', 'CG']:
                valid_segments.extend([True, True])
            else:
                valid_segments.extend([False, False])
        else:
            valid_segments.append(False)  # Single segment without a pair is considered invalid

    return valid_segments


# Save the player's created string
def saveString(string):
    with open('snake_scores.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([string])


# Randomly generate a new food source in a specified region, represented as an array
def generateRandomFood(min_x, max_x, min_y, max_y):
    # Create an array representing rectangle in a random location
    coords = [round(random.randrange(min_x, max_x - block_size) / 10.0) * 10.0,
              round(random.randrange(min_y, max_y - block_size) / 10.0) * 10.0,
              block_size,
              block_size]

    # Randomly choose a food type
    nucleotide = ord(random.choice(list(nucleotide_colours.keys())))

    return coords + [nucleotide]


def gameLoop():
    # Used to end the game
    game_over = False
    game_lost = False
    game_close = False
    saved = False

    # Position the snake in the middle
    x1 = width / 2
    y1 = playable_height / 2

    # Initialize the variables for changing the snake's location
    x1_change = 0
    y1_change = 0

    # Initialize the snake variables
    snake_segments = []
    segment_nucleotides = 'A'  # Starting nucleotide of the snake
    snake_length = 1

    # Randomly place food items
    food_one = generateRandomFood(0, width, 0, playable_height)
    food_one[4] = ord('T')

    food_two = generateRandomFood(0, width, 0, playable_height)

    # Main game loop
    while not game_over:
        # Loops when the game has ended until the player responds
        while game_close:
            game_display.fill(colours['white'])
            # Prevents duplicate lines being saved
            if not saved:
                if len(snake_segments) > 7:
                    saveString(segment_nucleotides)
                saved = True

            if game_lost:
                showText("You lost! Press Q-Quit or C-Play Again", colours['red'], width / 6, playable_height / 3)
            else:
                showText("You completed the sequence!", colours['green'], width / 6, playable_height / 3)
                showText("Press Q-Quit or C-Play Again", colours['green'], width / 6, playable_height / 3 + block_size)
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
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = block_size
                    x1_change = 0

        # Check if the snake collides with the outer walls end the game
        if x1 >= width or x1 < 0 or y1 >= playable_height or y1 < 0:
            game_lost = True
            game_close = True

        # If the string reaches length of 30 the player wins
        if len(segment_nucleotides) > 29:
            game_close = True

        # Update display
        game_display.fill(colours['white'])

        # Draw food item with the current color and nucleotide character
        pygame.draw.rect(game_display, colours[nucleotide_colours[chr(food_one[4])]], food_one[:4])
        showText(chr(food_one[4]), colours['black'], food_one[0], food_one[1])
        pygame.draw.rect(game_display, colours[nucleotide_colours[chr(food_two[4])]], food_two[:4])
        showText(chr(food_two[4]), colours['black'], food_two[0], food_two[1])

        # Draw GUI
        pygame.draw.line(game_display, colours['black'], (0, 320), (600, 320))
        valid_segments = checkNucleotideString(segment_nucleotides)  # Get validity of characters in string

        # Draw each character on the screen
        for i, segment in enumerate(segment_nucleotides):
            # Determine the color based on segment validity
            color = colours['red'] if not valid_segments[i] else colours['black']

            # Calculate position for each character
            x_pos = 0 + (i * block_size)
            y_pos = playable_height + ((height - playable_height) / 2)

            # Display each nucleotide with the determined color
            showText(segment, color, x_pos, y_pos)

        # Update snake
        x1 += x1_change
        y1 += y1_change
        snake_head = [x1, y1]
        snake_segments.append(snake_head)
        if len(snake_segments) > snake_length:
            del snake_segments[0]

        # Check if the snake collides with itself
        for x in snake_segments[:-1]:
            if x == snake_head:
                game_lost = True
                game_close = True

        # Draw the snake with segment-specific colors and DNA nucleotides
        for i, segment in enumerate(snake_segments):
            pygame.draw.rect(game_display, colours[nucleotide_colours[segment_nucleotides[i]]],
                             [segment[0], segment[1], block_size, block_size])
            showText(segment_nucleotides[i], colours['black'], segment[0], segment[1])

        pygame.display.update()

        # Check if the food is eaten by the snake
        if block_collision(x1, y1, food_one[0], food_one[1], block_size) or block_collision(x1, y1, food_two[0], food_two[1], block_size):
            # Add food that has been eaten to the snake, the if statement ensure it's the correct one
            if x1 < food_one[0] + block_size and x1 + block_size > food_one[0] and y1 < food_one[1] + block_size:
                # Add the current food color to the new segment
                segment_nucleotides += chr(food_one[4])
            else:
                # Add the current food color to the new segment
                segment_nucleotides += chr(food_two[4])

            # Reposition the food and update snake
            food_one = generateRandomFood(0, width, 0, playable_height)
            food_two = generateRandomFood(0, width, 0, playable_height)
            snake_length += 1

            if not len(checkNucleotideString(segment_nucleotides)) % 2:
                # If there are no incomplete pairs, begin the next one
                food_one[4] = ord(random.choice(list(nucleotide_colours.keys())))
                food_two[4] = ord(random.choice(list(nucleotide_colours.keys())))

            else:
                # Provide a correct answer for the player
                last_char = segment_nucleotides[-1:]

                # Set food nucleotide to matching pair
                if last_char == 'A':
                    food_one[4] = ord('T')
                elif last_char == 'T':
                    food_one[4] = ord('A')
                elif last_char == 'G':
                    food_one[4] = ord('C')
                else:
                    food_one[4] = ord('G')

        checkNucleotideString(segment_nucleotides)
        clock.tick(snake_speed)

    pygame.quit()
    print(segment_nucleotides)
    quit()


gameLoop()
