def main():
    plate = input("Plate: ")

    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):
    if len(s) > 6 or len(s) < 2:
        return False
    elif not s.isalnum():
        return False
    elif not s[:2].isalpha():
        return False
    # call check function to check if number contains in the middle of the plate and if the first number starts with 0
    elif check(s):
        return False
    else:
        return True


def check(s):

    # starts from the third digit, once a number find and is zero, will return ture
    # looping through from third digit to second last digit,
    # if it is number and it is next digit is not number will return true
    for i in s[2:-1]:
        if i.isdecimal() and i == "0":
            return True
        elif i.isdecimal() and s[s.index(i)+1].isalpha():
            return True
        else:
            continue
    return False

if __name__ == "__main__":
    main()
