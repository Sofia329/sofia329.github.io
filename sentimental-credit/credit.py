from cs50 import get_string
import re

def main():

    card_number = get_string("Number: ")

    if not luhn_algo(card_number):
        print("INVALID")
        return

    # check if digit no. & begin digit both valid
    if re.match(r"3[47]\d{13}$", card_number):
        print("AMEX")
    elif re.match(r"5[1-5]\d{14}$", card_number):
        print ("MASTERCARD")
    elif re.match(r"4(\d{12}|\d{15})$", card_number):
        print("VISA")
    else:
        print("INVALID")


# check if checksum is valid
def luhn_algo(card):

    total = 0

    for i in card[-2::-2]:
        i = int(i)
        if i * 2 > 9:
            total += (i * 2) % 10 + (i * 2)//10
        else:
            total += (i * 2)

    for i in card[::-2]:
        total += int(i)


    return total % 10 == 0


if __name__ ==  "__main__":
    main()
