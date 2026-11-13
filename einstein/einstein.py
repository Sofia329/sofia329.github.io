
def main():
    a = input("m: ")
    print(convert(a))

def convert(mass):
    mass = int(mass)
    energy = 300000000 ** 2 * mass
    return energy



if __name__ == "__main__":
    main()
