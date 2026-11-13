import sys
import random
from pyfiglet import Figlet


def main():

    figlet = Figlet()

    try:

        if len(sys.argv) == 1:
            a = random.choice(figlet.getFonts())
            figlet.setFont (font = a)

        elif sys.argv[1] != "-f" and sys.argv[1] != "--font":
            sys.exit("Invalid Usage")

        elif sys.argv[2] not in figlet.getFonts():
            print("test2")
            sys.exit("Invalid Usage")

        else:
            figlet.setFont(font = sys.argv[2])

        str = input("Input: ")

        print(figlet.renderText(str))

    except (IndexError, ValueError) as e:
        print(f"Something wrong: {e}")






if __name__ == "__main__":
    main()
