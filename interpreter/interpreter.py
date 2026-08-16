def main():
    equation = input (" ")
    a = math(equation)
    print(f"{a:.1f}")

def math(equation):
    a,b,c = equation.split(" ")
    a = int(a)
    c = int(c)

    if b == "+":
        return (a + c)
    elif b == "-":
        return (a - c)
    elif b == "*":
        return (a * c)
    else:
        return (a / c)

if __name__ == "__main__":
    main()
