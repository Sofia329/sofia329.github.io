from numb3rs import validate

def test_validate1():
    #test to ensure none # are starting with 0 and then decimal digit, except 0 standalone
    assert validate("000.10.8.9") == False
    assert validate ("10.01.02.4") == False
    assert validate ("0.0.0.0") == True


def test_validate2():
    # test to ensure if more than 4 of # will be rejected, as well as none of # shld not between 0 and 255 will be rejected
    assert validate("275.2.3.4") == False
    assert validate("255.4.5.6.7") == False
    assert validate("-3.4.5.6") == False
    assert validate("205.275.3.4") == False

def test_validate3():
    # test to ensure if more than 4 of # will be rejected, as well as none of # shld not between 0 and 255 will be rejected
    assert validate("275.244.36.45.67") == False
    assert validate("2001:0db8:85a3:0000:0000:8a2e:0370:7334") == False
    assert validate("-3.4.5.$6") == False
    assert validate("205.275.3.4.6.7.8.9") == False
    assert validate("8.8.8") == False
    assert validate("cat") == False
