import pytest
from fuel import convert, gauge

def test_convert():
    assert convert("3/4") == 75
    with pytest.raises (ValueError):
        convert ("three/four")
    with pytest.raises (ZeroDivisionError):
        convert ("3/0")
    with pytest.raises (ValueError):
        convert ("5/4")
    with pytest.raises (ValueError):
        convert ("-5/4")


def test_gauge():
    assert gauge(75) == "75%"
    assert gauge(25) == "25%"
    assert gauge(99) == "F"
    assert gauge(1) =="E"
