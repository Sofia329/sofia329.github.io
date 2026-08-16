def main():
    words = input("Greeting: ").strip(" ")
    a = value(words)
    print(a)

def value(greeting):
    words = greeting.lower()

    if "hello" in words:
        return 0
    elif words[0] == "h":
        return 20
    else:
        return 100


if __name__ == "__main__":
    main()
