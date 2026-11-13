def main():
    words = input("Greeting: ")
    a = greeting(words)
    print(a)

def greeting(words):
    words = words.lower()
    if "hello" in words:
        return ("$0")
    elif words[0] == "h":
        return ("$20")
    else:
        return ("$100")

if __name__ == "__main__":
    main()

