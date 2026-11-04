"""Task 2: tests in a SEPARATE file (pytest).

Read the rules at the top of refund.py, then replace every ____
with the refund you EXPECT. Do not read the code of refund() yet!
"""
from refund import refund


# Example - already done for you
def test_short_delay_gives_nothing():
    assert refund(80.0, 30) == 0.0


def test_delay_90_minutes():
    assert refund(80.0, 90) == ____


def test_delay_exactly_60_minutes():
    assert refund(80.0, 60) == ____


def test_delay_150_minutes():
    assert refund(80.0, 150) == ____


def test_small_refund_is_not_paid():
    assert refund(12.0, 90) == ____


# Your own test: a refund of exactly 4.00 euro IS paid out.
# Pick a ticket price and a delay that give exactly 4.00.
def test_exactly_4_euro_is_paid():
    assert refund(____, ____) == 4.0
