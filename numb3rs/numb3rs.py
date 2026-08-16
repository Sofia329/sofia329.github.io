import re


def main():
    print(validate(input("IPv4 Address: ")))


def validate(ip):
    if match := re.search(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$", ip):
        for i in match.groups():
            if int(i) < 0 or int(i)>255:
                return False
        return True
    else:
        return False



if __name__ == "__main__":
    main()
