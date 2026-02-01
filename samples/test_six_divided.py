import pytest

# section1
def six_divided(x):
    return 6 / x

@pytest.mark.parametrize(
    "x, expected",
    [
        (4, 1.5),
        (3, 2.0),
        (2, 3.0),
        (1, 6.0),
    ]
)
def test_six_divided(x, expected):
    assert six_divided(x) == expected
# end

# section2
def test_six_divided_by_zero():
    with pytest.raises(ZeroDivisionError):
        six_divided(0)
# end

# section3
@pytest.mark.parametrize(
    "x, expected_error",
    [
        (0, ZeroDivisionError),
        ("cat", TypeError),
    ]
)
def test_six_divided_errors(x, expected_error):
    with pytest.raises(expected_error):
        six_divided(x)
# end
