
import sys
import csv

def main():
    if len(sys.argv) < 3:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")
    elif not sys.argv[1].endswith(".csv"):
        sys.exit("Could not read invalid_file.csv")

    #open before.csv for read
    try:
        with open (sys.argv[1]) as file:
            reader = csv.DictReader(file)
            student = [row for row in reader] # a list of dictionaries [{}, {}]

        #create after.csv for write
        with open (sys.argv[2], "w") as file:
            writer = csv.DictWriter(file, fieldnames = ["first","last","house"])
            writer.writeheader()
            for i in student:
                try:
                    last, first = i["name"].split(",")
                    writer.writerow(
                        {"first": first.strip(),
                         "last": last.strip(),
                         "house": i["house"]}
                    )

                except ValueError:
                    print("no comma in the name to split")
                    continue

    except FileNotFoundError:
        sys.exit("file not valid")


if __name__ == "__main__":
    main()
