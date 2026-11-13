import sys
from datetime import date
import inflect


def main():
    b_day = input ("Date of Birth: ")

    #call the function to calculate how many minutes lives
    age_in_mins = calculator_mins (b_day)

    #call the function to convert mins to words
    words = convert_mins(age_in_mins)

    print (f"{words} minutes")


def calculator_mins(b_day):

    try:
        #reformat string input to a date object format
        b_day = date.fromisoformat(b_day)

    except ValueError:
        sys.exit("Input Date is not the form of YYYY-MM-DD")

    #calculate how many days between user's birthday and today
    diff_days = date.today() - b_day # two datetime object minus will return a timedelta type

    #convert to min
    print(24 * 60 * diff_days.days)
    return 24 * 60 * diff_days.days # will return as int


def convert_mins(mins):
    p = inflect.engine()
    words = p.number_to_words(mins, andword = "")
    return words.capitalize() # output only first letter is capital


if __name__ == "__main__":
    main()



