"""Task 3: be the independent tester - try to BREAK refund()."""
import pytest

from refund import refund


# Part A: one test function, many cases.
# Test just below, exactly at and just above every border.
@pytest.mark.parametrize("delay, expected", [
    (59, 0.0),
    (60, 20.0),
    (119, ____),
    (120, ____),
])
def test_borders(delay, expected):
    assert refund(80.0, delay) == expected


# Part B: bad input must be rejected with a ValueError.
def test_negative_price_is_rejected():
    with pytest.raises(ValueError):
        refund(-80.0, 90)


def test_negative_delay_is_rejected():
    ____  # write this test yourself (look at the one above)
