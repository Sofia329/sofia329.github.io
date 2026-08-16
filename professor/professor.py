import random


def main():
    level = get_level()
    score = 0

    for i in range(10):
            x = generate_integer(level)
            y = generate_integer(level)

            ans = x + y

            for i in range (3):
                try:
                    result = int(input(f"{x} + {y} = "))
                    if result == ans:
                        score += 1
                        break
                    else:
                        print("EEE")
                except ValueError:
                    pass
            else:
                print (f"{x} + {y} = {ans}")

    print (f"Score: {score}")


def get_level():

    while True:
        try:
            level = int(input("Level: "))
            if level in range (1,4):
                return level
        except ValueError:
            pass


def generate_integer(level):

    if level == 1:
        return random.randint(0,9)
    elif level == 2:
        return random.randint(10,99)
    else:
        return random.randint(100,999)


if __name__ == "__main__":
    main()
