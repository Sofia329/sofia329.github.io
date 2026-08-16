import emoji


def main():

    try:
        a = input("Input: ")
        sub_a = a[a.index(":"): ]
        b = emoji.emojize(sub_a, language = "alias")
        c = a[ : a.index(":")]
        print(f"{c}{b}")

    except ValueError as e:
        print(f"{e}")




if __name__ == "__main__":
    main()

