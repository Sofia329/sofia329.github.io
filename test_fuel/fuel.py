def main():

    #now handling error
    while True:
        try:
            fraction = input("fraction: ")
            percentage = convert(fraction)
            print(gauge(percentage))
            break
        except (ValueError, ZeroDivisionError):
            print('enter again')
            continue


def convert(value): # turn string into percentage
    try:
        x_str, y_str  = value.split('/')
    except ValueError:
        raise ValueError("Cannot Split")

    try:
        x = int(x_str)
        y = int(y_str)
    except ValueError:
        raise ValueError("Need to be Integer")

    if y == 0:
        raise ZeroDivisionError("Denominator cannot be zero")
    if x < 0 or y < 0 or x > y:
        raise ValueError ("Invalid Fraction")

    percentage = x/y
    return percentage * 100


def gauge(percentage):

    if percentage <= 1:
        return "E"
    if percentage >= 99:
        return "F"

    return f"{percentage:.0f}%"


if __name__ == "__main__":
    main()
