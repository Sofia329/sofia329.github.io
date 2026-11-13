import random


def main():

    while True:

        try:
            level = int(input("Level: "))
            if level <= 0:
                continue
            else:
                break

        except ValueError:
            continue

    guess(level)


def guess(level):

    n = random.randint(1, level)

    while True:

        try:
            guess = int(input("Guess: "))

            if guess <= 0:
                raise ValueError

            elif guess < n:
                print("Too Small!")
                continue
            elif guess > n:
                print("Too large!")
                continue
            else:
                print("just right!")
                return

        except ValueError:
            continue


if __name__ == "__main__":
    main()
