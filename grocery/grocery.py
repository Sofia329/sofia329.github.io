def main():
    dict = grocery_list()
    for key, value in dict.items():
        print(f"{value} {key}")

def grocery_list():
    items = {}
    while True:
        try:
            item = input("").upper()
            if item in items:
                items[item] += 1
            else:
                items[item] = 1

        except EOFError:
            break

    sorted_dict = dict(sorted(items.items()))

    return sorted_dict


if __name__ == "__main__":
    main()
