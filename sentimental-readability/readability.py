from cs50 import get_string

def main():
    paragraph = get_string("Text: ")

    word_count = words(paragraph)
    letter_count = letters(paragraph)
    sentence_count = sentences(paragraph)

    #compute reading grade
    grade = round(0.0588 * letter_count/word_count*100 - 0.296 * sentence_count/word_count*100 - 15.8)

    if grade >= 16:
        print("Grade 16+")
    elif grade < 1:
        print("Before Grade 1")
    else:
        print(f"Grade: {grade}")


def words(text):
    count = 0
    for i in text:
        if i == " ":
            count += 1
    return count + 1

def letters(text):
    count = 0
    for i in text:
        if i.isalpha():
            count += 1
    return count

def sentences(text):
    count = 0
    for i in text:
        if i in ["!", ".", "?"]:
            count += 1
    return count

if __name__ == "__main__":
    main()
