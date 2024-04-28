import numpy as np
from PIL import Image
import hashlib
import matplotlib.pyplot as plt

image = Image.open('assets/player.png')
imageArray = np.asarray(image, dtype=np.uint8)
editableArray = imageArray.copy()


# Takes a combo of letters and returns a hex value which can be used as a colour,
# uses a hash function to get unique colours based on combinations
def pick_color(combination):
    # Hash the combination string
    hash_value = hashlib.sha256(combination.encode()).hexdigest()

    # Take the first 6 characters of the hash to form a hexadecimal color code
    colour_code = hash_value[:6]

    # Hex to RGB
    RGB = tuple(int(colour_code[i:i+2], 16) for i in (0, 2, 4)) + (150,)

    return RGB


# Primary colour clothes
clothes = [
        # Hat
        [0, 21], [0, 22],
        [1, 20], [1, 21], [1, 22], [1, 23], [1, 24],
        [2, 19], [2, 20], [2, 21], [2, 22], [2, 23], [2, 24], [2, 25],
        [3, 19], [3, 20], [3, 21], [3, 22], [3, 23], [3, 24], [3, 25], [3, 26],

        # Jacket
        [6, 15], [6, 16], [6, 17], [6, 18], [6, 19], [6, 20], [6, 21],
        [7, 14], [7, 15], [7, 16], [7, 17], [7, 18], [7, 19], [7, 20], [7, 21],
        [8, 13], [8, 14], [8, 15], [8, 16], [8, 17], [8, 18], [8, 19], [8, 20],
        [9, 12], [9, 13], [9, 14], [9, 15], [9, 16], [9, 17], [9, 18], [9, 19],
        [10, 11], [10, 12], [10, 13], [10, 14], [10, 15], [10, 16], [10, 17], [10, 18], [10, 19],
        [11, 10], [11, 11], [11, 12], [11, 13], [11, 14], [11, 15], [11, 16], [11, 17], [11, 18], [11, 19],
        [12, 9], [12, 10], [12, 11], [12, 12], [12, 13], [12, 14], [12, 15], [12, 16], [12, 17], [12, 18], [12, 19],
        [13, 9], [13, 10], [13, 11], [13, 12], [13, 13], [13, 14], [13, 15], [13, 16], [13, 17], [13, 18], [13, 19], [13, 20], [13, 21],
        [14, 10], [14, 11], [14, 12], [14, 13], [14, 14], [14, 15], [14, 16], [14, 18], [14, 19], [14, 20], [14, 21], [14, 22], [14, 23],
        [15, 11], [15, 12], [15, 13], [15, 14], [15, 15], [15, 16], [15, 19], [15, 20], [15, 21], [15, 22], [15, 23]]

secondaryClothes = [
        # Hood
        [4, 16], [4, 17],
        [5, 15], [5, 16], [5, 17], [5, 18],
        [6, 15], [6, 16], [6, 17], [6, 18], [6, 19],

        # Shoes
        [24, 13],
        [26, 16], [26, 17],
        [30, 15], [30, 16],
        [31, 15], [31, 16], [31, 17], [32, 18], [32, 19],
        [32, 15], [32, 16], [32, 17], [32, 18], [32, 19],

        # Bike box
        [13, 1], [13, 2], [13, 3], [13, 4], [13, 5], [13, 6], [13, 7], [13, 8], [13, 9],
        [14, 1], [14, 2], [14, 3], [14, 4], [14, 5], [14, 6], [14, 7], [14, 8], [14, 9],
        [15, 1], [15, 2], [15, 3], [15, 4], [15, 5], [15, 6], [15, 7], [15, 8], [15, 9],
        [16, 1], [16, 2], [16, 3], [16, 4], [16, 5], [16, 6], [16, 7], [16, 8], [16, 9],
        [17, 1], [17, 2], [17, 3], [17, 4], [17, 5], [17, 6], [17, 7], [17, 8], [17, 9],
        [18, 1], [18, 2], [18, 3], [18, 4], [18, 5], [18, 6], [18, 7], [18, 8], [18, 9],
        [19, 1], [19, 2], [19, 3], [19, 4], [19, 5], [19, 6], [19, 7], [19, 8], [19, 9],
        [20, 1], [20, 2], [20, 3], [20, 4], [20, 5], [20, 6], [20, 7], [20, 8], [20, 9],
]

bike = [
        [16, 27],
        [17, 27],
        [18, 24], [18, 25], [18, 26],
        [19, 17], [19, 18], [19, 19], [19, 20], [19, 21], [19, 22], [19, 23], [19, 24], [19, 25],
        [20, 24], [20, 25], [20, 26],
        [21, 1], [21, 2], [21, 9], [21, 12], [21, 23], [21, 24], [21, 26],
        [22, 2], [22, 8], [22, 9], [22, 11], [22, 12], [22, 23], [22, 26], [22, 27],
        [23, 3], [23, 8], [23, 11], [23, 22], [23, 23], [23, 27],
        [24, 4], [24, 8], [24, 10], [24, 22], [24, 28],
        [25, 4], [25, 8], [25, 9], [25, 10], [25, 21], [25, 28],
        [26, 5], [26, 8], [26, 9], [26, 20], [26, 21], [26, 28], [26, 29],
        [27, 5], [27, 8], [27, 20], [27, 29],
        [29, 9], [29, 10], [29, 11], [29, 12], [29, 13], [29, 14]

        ]


def main():
    with open('snake_scores.csv', 'r') as f:
        file = f.readlines()
    for line in file:
        dna = line[:24]

        # Render secondary clothes colour
        for each in secondaryClothes:
                editableArray[each[0], [each[1]]] = [pick_color(dna[8:16])]

        # Render primary clothes colour
        for each in clothes:
                editableArray[each[0], [each[1]]] = [pick_color(dna[:8])]

        # Render bike colour
        for each in bike:
                editableArray[each[0], [each[1]]] = [pick_color(dna[16:])]

        plt.imshow(editableArray)
        plt.show()

        img = Image.fromarray(editableArray, 'RGBA')
        img.save('assets/character_options/' + dna + '.png')
        img.close()


main()