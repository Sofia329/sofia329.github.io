
def main():
    camel_case = input("camelCase:")
    snake_case = ""


    #the normal for loop

    for letter in camel_case:
        if letter.isupper():
            snake_case += "_"
        snake_case += letter.lower()

    print(snake_case)


if __name__ == "__main__":
    main()
