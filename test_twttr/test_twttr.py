
from twttr import shorten

def test_shorten_1():
    assert shorten("Twitter") == "Twttr"
    assert shorten ("NICE Shot") == "NC Sht"


def test_shorten_2():
    assert shorten ("CS50") == "CS50"
    assert shorten ("Hello, World!") == "Hll, Wrld!"

def test_shorten_3():
    assert shorten ("HOW'RE YOU") == "HW'R Y"

