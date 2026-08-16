import inflect



def main():
    print(f"Adieu, adieu, to {adieu()}")

def adieu():
    a = []
    while True:
        try:
            #if user typed a sentence, it will be error with the capitalize
            name = input(" ").strip().capitalize()
            a.append(name)

        except EOFError:
            break

    if len(a) == 1:
        return a[0]
    elif len(a) == 2:
        return " and ".join(a)
    else:
        remove_last_name = a.pop()
        name_list = ", ".join(a)
        name_list = name_list + ", and " + remove_last_name
        return name_list



if __name__ == "__main__":
    main()


