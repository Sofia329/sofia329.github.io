def main():

    #now handling error
    while True:
        try:
            fraction = input("fraction: ")
            print(convert(fraction))
            break
        except (ValueError, ZeroDivisionError):
            print('enter again')
            continue


def convert(value): # turn string into percentage
    try:
        x_str, y_str  = value.split('/')
    except ValueError:
        raise ValueError

    try:
        x = int(x_str)
        y = int(y_str)
    except ValueError:
        raise ValueError ("Need to be Integer")

    if x > y:
        raise ValueError
    if x < 0 or y < 0:
        raise ValueError

    try:
        percentage = x/y

    except ZeroDivisionError:
        raise ZeroDivisionError ("Denominator cannot be Zero")

    if percentage <= 0.01:
        return "E"
    if percentage >= 0.99:
        return "F"

    return f"{percentage:.0%}"



if __name__ == "__main__":
    main()
