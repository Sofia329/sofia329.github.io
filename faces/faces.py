def main():
    a = input("pls input")
    print (convert(a))


def convert(a):
    b = a.replace(":)", "🙂").replace(":(","🙁")
    return b

main()
