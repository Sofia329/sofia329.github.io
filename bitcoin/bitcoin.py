import json
import sys
import requests


def main():
    try:
        bitcoin_no = float(sys.argv[1])
    except (ValueError, IndexError):
        sys.exit("Command Line Argument is not a number or Missing Argument")
    else:
        print(f"${get_api(bitcoin_no):,.4f}")

def get_api(bitcoin):
    try:
        key = {"apiKey": "474210baee7caf7b68df6ecb5a6b4c6e64b2d61a82e82c91924094150b7d595d"}
        my_link = requests.get("https://rest.coincap.io/v3/assets/bitcoin", params = key)
        price = float(my_link.json()["data"]["priceUsd"])
        return bitcoin * price
    except requests.RequestException:
        sys.exit()



if __name__ == "__main__":
    main()
