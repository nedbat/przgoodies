def is_even(n):
    return bool(n % 2 == 0)

def test_four_is_even():
    assert is_even(4)

def test_five_is_not_even():
    assert not is_even(5)
