import hashlib

import pygame
from PIL import Image

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 1500, 750
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption("DNA paperboy")
font_style = pygame.font.SysFont("C:/Windows/Fonts/Arial.ttf", 35)

# Define colors and their rgb values
colours = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (213, 50, 80),
    'green': (0, 255, 0),
    'blue': (50, 153, 213),
    'yellow': (255, 255, 0)
}

# Load the background images
background = pygame.image.load("assets/background.jpg").convert()
background_rect = background.get_rect()

character_background = pygame.image.load("assets/Characters_screenBG.png")

instructions = pygame.image.load("assets/Paperboy_Instructions.png").convert()

# Set up the player
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

# Define the houses to deliver to
houses = [
    # Top row
    pygame.Rect(16, 70, 99, 70),   # 1
    pygame.Rect(117, 70, 99, 70),  # 2
    pygame.Rect(221, 70, 99, 70),  # 3
    pygame.Rect(402, 70, 99, 70),  # etc
    pygame.Rect(504, 70, 99, 70),
    pygame.Rect(605, 70, 99, 70),
    pygame.Rect(705, 70, 99, 70),
    pygame.Rect(810, 70, 99, 70),
    pygame.Rect(911, 70, 99, 70),
    pygame.Rect(1011, 70, 99, 70),
    pygame.Rect(1115, 70, 99, 70),
    pygame.Rect(1215, 70, 99, 70),
    pygame.Rect(1315, 70, 99, 70),

    # Right most column
    pygame.Rect(1400, 142, 99, 70),
    pygame.Rect(1400, 241, 99, 70),
    pygame.Rect(1400, 345, 99, 70),
    pygame.Rect(1400, 451, 99, 70),
    pygame.Rect(1400, 554, 99, 70),
    pygame.Rect(1400, 659, 99, 70),

    # Second right column
    pygame.Rect(1263, 242, 99, 70),
    pygame.Rect(1263, 344, 99, 70),
    pygame.Rect(1263, 446, 99, 70),
    pygame.Rect(1263, 553, 99, 70),
    pygame.Rect(1263, 656, 99, 70),

    # Left most column
    pygame.Rect(50, 181, 91, 122),
    pygame.Rect(50, 336, 91, 122),
    pygame.Rect(50, 492, 91, 122),

    # Second left column
    pygame.Rect(191, 183, 91, 122),
    pygame.Rect(191, 337, 91, 122),
    pygame.Rect(191, 493, 91, 122),

    # Top Centre
    pygame.Rect(479, 225, 189, 93),
    pygame.Rect(721, 225, 189, 93),

    # Bottom centre
    pygame.Rect(488, 539, 189, 93),
    pygame.Rect(730, 538, 189, 93)]


# Used to display text to the user
def showText(msg, color, x, y):
    msg = font_style.render(msg, True, color)
    game_display.blit(msg, [x, y])


# Checks if the delivery is valid and which house it corresponds to
def checkDelivery(testRect, direction):
    testRect = testRect.copy()
    if direction == "up":
        testRect.move_ip(0, -50)
    if direction == "down":
        testRect.move_ip(0, 50)
    if direction == "left":
        testRect.move_ip(-50, 0)
    if direction == "right":
        testRect.move_ip(50, 0)

    for house in houses:
        if testRect.colliderect(house):
            return houses.index(house) + 1

    return -1


# Generates 10 numbers from the DNA sequence between 1 and 34, which is used as the paper route
def generate_numbers(dna):
    # Generate SHA-256 hash
    hashed = hashlib.sha256(dna.encode()).digest()

    # Convert hash to a list of integers
    integers = [int(byte) for byte in hashed]

    # Generate 10 numbers between 1 and 34 (inclusive)
    numbers = [(x % 34) + 1 for x in integers]

    return numbers[:10]


# Player select function
def playerSelect():
    game_display.fill(colours['white'])
    characterNo = 0
    charSelection = True
    forwardArrow = pygame.Rect(450, 175, 158, 158)
    backwardArrow = pygame.Rect(950, 175, 158, 158)
    playerSelection = ''

    while charSelection:
        # Takes last image generated from character selection
        with open('snake_scores.csv', 'r') as f:
            line = f.readlines()
            noCharacters = len(line)
            line = line[(characterNo - 1) % noCharacters]   # Extract filename

        playerSelection = line[:24]
        playerOnScreen = Image.open("assets/character_options/" + playerSelection + ".png")
        playerOnScreen = playerOnScreen.resize((300, 300))

        mode = playerOnScreen.mode
        size = playerOnScreen.size
        data = playerOnScreen.tobytes()

        playerOnScreen = pygame.image.fromstring(data, size, mode).convert_alpha()

        game_display.blit(character_background, (0, 0))
        game_display.blit(playerOnScreen, (600, 175))
        showText(line[:24], colours['black'], 570, 100)

        showText("The character's first eight genes: '" + playerSelection[:8] +
                 "' are expressed within the primary clothing colour", colours['black'], 50, 500)
        showText("The character's next eight genes: '" + playerSelection[8:16] +
                 "' are expressed within the secondary clothing colour", colours['black'], 50, 550)
        showText("The character's last eight genes: '" + playerSelection[16:] +
                 "' are expressed within the character's bike colour", colours['black'], 50, 600)
        showText("This is character no. " + str((characterNo % noCharacters) + 1) + " out of: " + str(noCharacters), colours['black'], 50,
                 650)

        pygame.display.update()

        # Waits for the player to input
        pygame.event.clear()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    charSelection = False
                    break
            if event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()
                if forwardArrow.collidepoint(mousePos):
                    characterNo -= 1
                elif backwardArrow.collidepoint(mousePos):
                    characterNo += 1
            break

    return playerSelection


# Displays instructions and logo
def displayInstructions():
    game_display.blit(instructions, (0, 0))  # Displays instructions
    pygame.display.update()

    # Waits for the player to move on by pressing esc
    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break


# Main game function
def main():
    # Used to end the game
    game_over = False
    game_close = False
    gameTime = 0

    displayInstructions()
    playerSelection = playerSelect()
    playerImg = pygame.image.load("assets/character_options/" + playerSelection + ".png")
    houseNumbers = generate_numbers(playerSelection)
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()

    # Main game loop
    while not game_over:
        player = pygame.Rect(370, 0, 20, 20)
        clock.tick(60)

        # After game completion
        while game_close:
            game_display.fill(colours['white'])
            showText("You won! With a time of: " + str(gameTime), colours['black'], width / 3, height / 2)
            showText("Press Q-Quit or C-Play Again", colours['green'], width / 3, (height / 2) + 50)
            pygame.display.flip()

            # Handle user input for endgame
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        main()

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

        # Paper delivery options
        deliveryNo = -1
        if keys[pygame.K_w]:
            deliveryNo = checkDelivery(player, "up")

        if keys[pygame.K_s]:
            deliveryNo = checkDelivery(player, "down")

        if keys[pygame.K_a]:
            deliveryNo = checkDelivery(player, "left")

        if keys[pygame.K_d]:
            deliveryNo = checkDelivery(player, "right")

        if deliveryNo >= 0:
            if deliveryNo in houseNumbers:
                houseNumbers.remove(deliveryNo)

        if len(houseNumbers) == 0:
            game_close = True
            gameTime = (pygame.time.get_ticks()-start_ticks)/1000

        # Fill the screen with white
        game_display.fill(colours['white'])

        # Draw the background
        game_display.blit(background, background_rect)

        # Draw road lines, used to see where you can move and for aesthetics
        for line in roads:
            pygame.draw.rect(game_display, colours['white'], line)

        # Draw the player
        game_display.blit(playerImg, player)

        # Draw highlight of houses to deliver to
        for house in houseNumbers:
            pygame.draw.rect(game_display, colours['white'], houses[house - 1], 3)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        pygame.time.Clock().tick(60)


main()

# Quit Pygame
pygame.quit()
