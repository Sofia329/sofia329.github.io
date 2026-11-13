import pytest
import sys
from seasons import calculator_mins, convert_mins


# def main():
#     test_calculator_mins()
#     test_convert_mins()


def test_calculator_mins():
    assert calculator_mins("1999-01-01") == 14430240
    assert calculator_mins("2001-01-01") == 13377600

def test_calculator_mins_invalid():

    with pytest.raises(SystemExit) as exc_info:
        calculator_mins("2009-1-1")
    assert "Input Date is not the form of YYYY-MM-DD" in str(exc_info.value)

    with pytest.raises(SystemExit) as exc_info:
        calculator_mins("February 2, 2019")
    assert "Input Date is not the form of YYYY-MM-DD" in str(exc_info.value)

def test_convert_mins():
    assert convert_mins(14430240) == "Fourteen million, four hundred thirty thousand, two hundred forty"
    assert convert_mins(13377600) == "Thirteen million, three hundred seventy-seven thousand, six hundred"


# if __name__ == "__main__":
#     main()


