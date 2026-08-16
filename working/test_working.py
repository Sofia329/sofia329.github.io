import pytest
from working import convert

# test if normal case work  as expected
def test_convert_1():
    assert convert("9:00 AM to 8:00 PM") == "09:00 to 20:00"
    assert convert("8 AM to 5 PM") == "08:00 to 17:00"
    assert convert("9:00 AM to 4:00 PM") == "09:00 to 16:00"
    assert convert("7 AM to 7:00 PM") == "07:00 to 19:00"

# test output if from am to am | from pm to pm |from pm to am
def test_convert_2():
    assert convert("9:00 AM to 10:00 AM") == "09:00 to 10:00"
    assert convert("9:00 PM to 11:00 PM") == "21:00 to 23:00"
    assert convert("4 PM to 5 AM") == "16:00 to 05:00"

# test if special case of 12pm or 12am

def test_convert_3():
    assert convert("12:00 AM to 3:00 PM") == "00:00 to 15:00"
    assert convert("12:00 PM to 5:45 AM") == "12:00 to 05:45"
    assert convert("12 PM to 12:00 AM") == "12:00 to 00:00"

def test_convert_4():
    with pytest.raises(ValueError):
        convert("9:00 AM 5:00 ") # omit to will raise error
    with pytest.raises(ValueError):
        convert("9:00 am to 5:00 pm")

def test_convert_5():
    with pytest.raises(ValueError):
        convert("10AM to 5PM")
    with pytest.raises (ValueError):
        convert("10AM to 5pm") # no space will raise error

def test_convert_6():
    with pytest.raises (ValueError):
        convert("9 to 4 PM") # missing am/pm will raise error
    with pytest.raises (ValueError):
        convert ("09:000 AM to 17:00 PM") # 000 can only match zero or two digits, so expect valueerror raised

def test_convert_7():
    with pytest.raises (ValueError):
        convert ("09:80 AM to 5:00 PM") # expect valueerror is mins over 60
    with pytest.raises (ValueError):
        convert("18:00 AM to 17:00 PM") # expect valueeror if hrs over 12
