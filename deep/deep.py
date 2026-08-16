def main():
    ans = input ("What is the Answer to the Great Question of Life, the Universe and Everything")
    a = words(ans)
    print(a)

def words(sentence):
    sentence = sentence.strip(" ").lower()

    if sentence == "42":
        return "Yes"
    elif sentence == "forty-two":
        return "Yes"
    elif sentence == "forty two":
        return "Yes"
    else:
        return "No"



if __name__ == "__main__":
    main()

