import sys
import os
from PIL import Image, ImageOps

def main():

    if len(sys.argv) < 3:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")

    suffix_1 = os.path.splitext(sys.argv[1])[1].lower()
    suffix_2 = os.path.splitext(sys.argv[2])[1].lower()

    if suffix_1 not in [".jpeg", ".jpg", ".png"] or suffix_2 not in [".jpeg", ".jpg", ".png"]:
        sys.exit("Invalid output")

    if suffix_1 != suffix_2:
        sys.exit("Input and output have different extensions")

    try:
        shirt = Image.open("shirt.png")

        with Image.open (sys.argv[1]) as before:
            resized = ImageOps.fit(before, shirt.size)
            resized.paste(shirt, shirt)
            resized.save(sys.argv[2])


    except FileNotFoundError:
        sys.exit("Input does not exist")



if __name__ == "__main__":
    main()
