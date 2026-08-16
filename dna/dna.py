import csv
import sys


def main():

    # Check for command-line usage
    if not len(sys.argv) == 3:
        print("Not Valid File")
        return

    # Read database file into a variable
    with open (sys.argv[1]) as csvfile:
        reader = csv.DictReader(csvfile)
        header = reader.fieldnames
        content = [row for row in reader]



    # Read DNA sequence file into a variable
    with open(sys.argv[2]) as txt:
        sequence = txt.read()

    # Find longest match of each STR in DNA sequence
    dna = {}
    for i in header[1:]:
        dna[i] = str(longest_match(sequence,i))


    # Check database for matching profiles
    for i in content:
        #each i is a dict, compares with dna dict if match
        match = True
        for key in dna.keys():
            if dna[key] != i[key]:
                match = False
                break
        if match:
            print(i["name"])
            return
    print("No Match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in sequence, return longest run found
    return longest_run


main()
