def main():
    time = input ("What time is it: ")
    a = convert(time)

    if a >= float(7) and a <= float(8):
        print("breakfast time")
    elif a >=float(12) and a<=float(13):
        print("lunch time")
    elif a >=float(18) and a<=float(19):
        print("dinner time")
    else:
        print ("")

def convert(time):
    hour , mins = time.split (":")
    return int(hour) + int(mins)/60


if __name__ == "__main__":
    main()

