from bank import value


def test_value1():
    assert value("hello") == 0
    assert value ("Hello") == 0

def test_value2():
    assert value ("How are you") == 20
    assert value ("how is going") == 20

def test_value3():
    assert value ("very good") == 100
    assert value ("ok, fine") == 100
