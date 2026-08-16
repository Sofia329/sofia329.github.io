def main():
    a = input("Input: ")
    print(f"Output: {call(a)}")


def shorten(word):
    pool = ["A", "E", "I", "O", "U", "a","e","i","o","u"]
    for i in word:
        if i in pool:
            word = word.replace(i, "")
    return word

if __name__ == "__main__":
    main()


