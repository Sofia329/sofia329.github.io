def main():

    amount_due = 50

    while True:
        amount = int(input("Insert Coin: "))
        if amount not in [25,10,5]:
            print(f"Amount Due: {amount_due}")
            continue

        while amount_due > 0:
            amount_due -=amount
            if amount_due == 0:
                print(f"Change Owed: {amount_due}")
                return
            elif amount_due < 0:
                print(f"Change Owed: {abs(amount_due)}")
                return
            else:
                print(f"Amount Due: {amount_due}")
                break


if __name__ == "__main__":
    main()

