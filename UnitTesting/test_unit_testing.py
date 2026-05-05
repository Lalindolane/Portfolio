# test_unit_testing.py
"""Python Essentials: Unit Testing.
<Lane Lindstrom>
<Math 345>
<01/29/2026>
"""

import unit_testing
import pytest


def test_add():
    assert unit_testing.add(1, 3) == 4, "failed on positive integers"
    assert unit_testing.add(-5, -7) == -12, "failed on negative integers"
    assert unit_testing.add(-6, 14) == 8

def test_divide():
    assert unit_testing.divide(4, 2) == 2, "integer division"
    assert unit_testing.divide(5, 4) == 1.25, "float division"
    with pytest.raises(ZeroDivisionError) as excinfo:
        unit_testing.divide(4, 0)
    assert excinfo.value.args[0] == "second input cannot be zero"


# Problem 1: write a unit test for unit_testing.smallest_factor(), then correct it.
def test_smallest_factor():
    # Make sure to test the edge case where we need to test the square root of n
    # (it isn't included in the range portion so will fail the code as stands)
    assert unit_testing.smallest_factor(7) == 7, "7"
    assert unit_testing.smallest_factor(2) == 2, "2"
    assert unit_testing.smallest_factor(10) == 2, "10"
    assert unit_testing.smallest_factor(4) == 2, "4"
    assert unit_testing.smallest_factor(1) == 1, "1"

# Problem 2: write a unit test for unit_testing.month_length().
def test_month_length():
    # Tests all possible outputs of month_length() from unit_testing
    assert unit_testing.month_length("september") is None, "lowercase fails"
    assert unit_testing.month_length("September") == 30
    assert unit_testing.month_length("January") == 31
    assert unit_testing.month_length("February") == 28
    assert unit_testing.month_length("February", leap_year=True) == 29


# Problem 3: write a unit test for unit_testing.operate().
def test_operate():
    # Tests all possible outputs of operate from unit_testing
    assert unit_testing.operate(1, 5, "+") == 6
    assert unit_testing.operate(1, 5, "-") == -4
    assert unit_testing.operate(1, 5, "*") == 5
    assert unit_testing.operate(1, 5, "/") == .2
    with pytest.raises(ZeroDivisionError) as excinfo:
        unit_testing.operate(1, 0, '/')
    with pytest.raises(TypeError) as excinfo:
        unit_testing.operate(1, 5, 7)
    with pytest.raises(ValueError) as excinfo:
        unit_testing.operate(1, 5, '5')


# Problem 4: write unit tests for unit_testing.Fraction, then correct it.
@pytest.fixture
def set_up_fractions():
    # Sets up some Fraction classes from unit_testing for testing
    frac_1_3 = unit_testing.Fraction(1, 3)
    frac_1_2 = unit_testing.Fraction(1, 2)
    frac_n2_3 = unit_testing.Fraction(-2, 3)
    return frac_1_3, frac_1_2, frac_n2_3


def test_fraction_init(set_up_fractions):
    # Tests the initialization of Fraction from unit_testing
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert frac_1_3.numer == 1
    assert frac_1_2.denom == 2
    assert frac_n2_3.numer == -2
    frac = unit_testing.Fraction(30, 42)
    assert frac.numer == 5
    assert frac.denom == 7
    with pytest.raises(ZeroDivisionError) as excinfo:
        unit_testing.Fraction(1, 0)
    with pytest.raises(TypeError) as excinfo:
        unit_testing.Fraction(.2, 5)
    with pytest.raises(TypeError) as excinfo:
        unit_testing.Fraction(1, .1)


def test_fraction_str(set_up_fractions):
    # Tests the string method on Fraction from unit_testing
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert str(frac_1_3) == "1/3"
    assert str(frac_1_2) == "1/2"
    assert str(frac_n2_3) == "-2/3"
    assert str(unit_testing.Fraction(2, 1)) == "2"


def test_fraction_float(set_up_fractions):
    # Tests the float method on Fraction from unit_testing
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert float(frac_1_3) == 1 / 3.
    assert float(frac_1_2) == .5
    assert float(frac_n2_3) == -2 / 3.


def test_fraction_eq(set_up_fractions):
    # Tests == comparison of Fraction class from unit_testing
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert frac_1_2 == unit_testing.Fraction(1, 2)
    assert frac_1_3 == unit_testing.Fraction(2, 6)
    assert frac_n2_3 == unit_testing.Fraction(8, -12)
    assert unit_testing.Fraction(1, 2) == .5


def test_fraction_add(set_up_fractions):
    # Tests addition  on the Fraction class from unit_testing
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert frac_1_3 + frac_1_2 + frac_n2_3 == 1 / 6


def test_fraction_sub(set_up_fractions):
    # Tests subtraction on the Fraction class from unit_testing
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert frac_1_2 - frac_1_3 == 1/6


def test_fraction_mul(set_up_fractions):
    # Tests multiplication on the Fraction class from unit_testing
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert frac_1_2 * frac_1_3 == 1/6


def test_fraction_truediv(set_up_fractions):
    # Tests true division on the Fraction class from unit_testing
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert frac_1_2 / frac_1_3 == 3/2
    with pytest.raises(ZeroDivisionError) as excinfo:
        unit_testing.Fraction(2, 6) / unit_testing.Fraction(0, 2)


# Problem 5: Write test cases for Set.
def test_count_sets():
    # Tests count_sets from unit_testing
    hand1 = ["1022", "1122", "0100", "2021",
            "0010", "2201", "2111", "0020",
            "1102", "0200", "2110", "1020"]
    assert unit_testing.count_sets(hand1) == 6
    with pytest.raises(ValueError) as excinfo:
        unit_testing.count_sets(['1230'])
    with pytest.raises(ValueError) as excinfo:
        unit_testing.count_sets(['1230', '1230', '1230', '1230', '1230', '1230', '1230', '1230', '1230', '1230', '1230', '1230'])
    with pytest.raises(ValueError) as excinfo:    
        unit_testing.count_sets(['0000', '0030', '1120', '1223', '1233', '3230', '2230', '1330', '1130', '1220', '1231', '123'])
    with pytest.raises(ValueError) as excinfo:    
        unit_testing.count_sets(['0000', '0030', '1120', '1223', '1233', '3230', '2230', '1330', '1130', '1220', '1231', '1234'])


def test_is_set():
    # Tests is_set from unit_testing
    a, b, c = '1022', '1122', '1020'
    assert unit_testing.is_set(a, b, c) is False
    a, b, c = '1230', '2230', '3230'
    assert unit_testing.is_set(a, b, c) is True