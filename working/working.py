import re


def main():
        print(convert(input("Hours: ")))

def convert(s):
    # Define the regex pattern to match valid input
    # This pattern requires spaces around "to" and proper AM/PM
    pattern = r"^(\d{1,2}):?(\d{2})?\s(AM|PM)\sto\s(\d{1,2}):?(\d{2})?\s(AM|PM)$"

    if match := re.search(pattern, s):
        h1, m1, ampm1, h2, m2, ampm2 = match.groups("0")

        # Convert to integers
        h1, m1 = int(h1), int(m1)
        h2, m2 = int(h2), int(m2)
        ampm1, ampm2 = ampm1, ampm2

        # Validate hours and minutes
        if h1 > 12 or h2 > 12:
            raise ValueError("Hours must be between 1 and 12")
        if m1 >= 60 or m2 >= 60:
            raise ValueError("Minutes must be between 0 and 59")

        # Convert to 24-hour format
        if ampm1 == "PM" and h1 != 12:
            h1 += 12
        elif ampm1 == "AM" and h1 == 12:
            h1 = 0

        if ampm2 == "PM" and h2 != 12:
            h2 += 12
        elif ampm2 == "AM" and h2 == 12:
            h2 = 0

        # Format the output
        return f"{h1:02d}:{m1:02d} to {h2:02d}:{m2:02d}"
    else:
        # If the input does not match the pattern at all, raise ValueError
        raise ValueError("Invalid input format")

if __name__ == "__main__":
    main()
