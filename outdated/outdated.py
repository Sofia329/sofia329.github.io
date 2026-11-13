def main():
    print(convert())

def convert():

    b =["January", "February","March","April","May","June","July","August","September","October","November","December"]

    while True:
        try:
            a = input ("Date: ").strip().capitalize()

            # if in the format of 9/8/1976

            if "/" in a:
                month, day, year = a.split("/")
                day = int(day)
                month = int(month)

                if month > 12 or day > 31:
                    raise ValueError
                date = f"{year}-{month:02}-{day:02}"
                return date

            #otherwise in the format of Dec 8, 2000 or December 8, 2000, or 8 December, 2000
            elif "," in a:
                year = a[-4:]
                day = a.removesuffix(str(year)).strip(" ,")
                for i in b:
                    if i in a or i[:3] in a:
                        day = day.replace(i, "").strip()
                        month = b.index(i)+1
                        break
                if int(day) > 31 or month > 12:
                    raise ValueError

                return f"{year}-{month:02}-{int(day):02}"

            else:
                raise ValueError


        except ValueError as e:
            print(f"Enter Again: {e}")
            continue



if __name__ == "__main__":
    main()




