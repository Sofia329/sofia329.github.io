
from plates import is_valid

#testing if length fulfils requirement
def test_plates_1():
    assert is_valid("H") == False
    assert is_valid("Hello, World!") == False
    assert is_valid("5") == False
    assert is_valid("HH54609") == False

#testing if first two are letters fulfils requirement
def test_plates_2():
    assert is_valid("HHOIU9") == True
    assert is_valid("H7890") == False

#testing if no zero begins & no numbers in between
def test_plates_3():
    assert is_valid("HH0989") == False
    assert is_valid("IIU89U") == False
    assert is_valid("II8934") == True
    assert is_valid("Hello9") == True

# checking no alphanumeric char
def test_plates_4():
    assert is_valid("hhi98!") == False
    assert is_valid ("HHI*") == False




