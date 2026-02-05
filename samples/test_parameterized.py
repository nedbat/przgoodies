def is_even(n):
    return n % 2 == 0

import pytest

@pytest.mark.parametrize(
    "n, expected",
    [
        (4, True),
        (5, False),
        (0, True),
        (-3, False),
    ],
)
def test_is_even(n, expected):
    assert is_even(n) is expected
