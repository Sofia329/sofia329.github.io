from um import count


def test_count_1():
    assert count("Um, thanks for the album.") == 1
    assert count("Um, emm, um, umm umm, um") == 3

