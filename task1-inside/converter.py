"""Task 1: tests INSIDE the file (doctest).

Remember the Celsius converter from the Docker tutorial?
The same bug is back - this time in Python.
"""


def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit.

    Each >>> line is a test. Python runs it and
    checks the result on the next line.

    >>> celsius_to_fahrenheit(0)
    32.0
    """
    return celsius * (9 // 5) + 32.0
