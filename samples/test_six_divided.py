import pytest

# section1
def six_divided(x):
    return 6 / x

# Check the happy paths

@pytest.mark.parametrize(
    "x, expected",
    [
        (4, 1.5),
        (3, 2.0),
        (2, 3.0),
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

# Check the error paths

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


from contextlib import nullcontext as produces
from pytest import raises

@pytest.mark.parametrize(
    "x, result",
    [
        (4,     produces(1.5)),
        (3,     produces(2.0)),
        (2,     produces(3.0)),
        (0,     raises(ZeroDivisionError)),
        ("cat", raises(TypeError)),
    ],
)
def test_division(x, result):
    with result as expected:
        assert six_divided(x) == expected
