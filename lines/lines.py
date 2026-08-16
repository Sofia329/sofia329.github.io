import sys


def main():

    if len(sys.argv) < 2:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 2:
        sys.exit("Too many command-line arguments")
    elif not sys.argv[1].endswith(".py"):
        sys.exit("Not a Python file")

    try:
        a = 0
        with open(sys.argv[1]) as file:
            for line in file:
                a += 1
                if line.strip().startswith ("#"):
                    a -= 1
                elif line.strip() == "":
                    a -= 1
            print(a)


    except FileNotFoundError:
        sys.exit("File not exist")

if __name__ == "__main__":
    main()
