""" four or more functions to collectively test the implementation of Jar"""
""" each begins with test_"""
import pytest

from jar import Jar

def test_init():
    jar = Jar(10)
    assert jar.capacity == 10
    assert jar.size == 0
    jar = Jar()
    assert jar.capacity == 12
    assert jar.size == 0

def test_str():
    jar = Jar()
    assert str(jar) == ""
    jar = Jar()
    jar.size = 5
    assert str (jar) == "🍪🍪🍪🍪🍪"

def test_deposit():
    jar = Jar(10)
    jar.deposit(5)
    assert jar.size == 5
    jar.deposit(2)
    assert jar.size == 7
    with pytest.raises (ValueError):
        jar.deposit(5)

def test_withdraw():
    jar = Jar(10)
    jar.deposit(10)
    jar.withdraw(10)
    assert jar.size ==0
    with pytest.raises (ValueError):
        jar.withdraw (1)

def test_capacity():
    jar = Jar()
    assert jar.capacity == 12
    jar = Jar(20)
    assert jar.capacity == 20
    with pytest.raises (ValueError):
        Jar(-1)
    with pytest.raises (ValueError):
        Jar("Zero")






