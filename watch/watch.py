import re
import sys


def main():
    print(parse(input("HTML: ")))


def parse(s):
    # check if user input url is correct first, e.g. contains www.youtube.com

    if match := re.search (r"^<iframe.*src=\"https?://(?:www\.)?youtube\.com/embed/(\w*).*</iframe>$", s):

        return ("https://youtu.be/" + match.group(1))

    else:

        return


if __name__ == "__main__":
    main()
