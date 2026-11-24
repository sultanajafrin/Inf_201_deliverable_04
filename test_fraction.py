import pytest

from fraction import Fraction


def test_init_reduces():
    """Checks if fractions are stored as reduced and that the denominator defaults to one"""
    f = Fraction(2, 4)
    assert (f.numerator, f.denominator) == (1, 2)
    assert Fraction(3).denominator == 1
    assert (Fraction(0, 5).numerator, Fraction(0, 5).denominator) == (0, 1)


def test_init_rejects_non_integers():
    """checks that both parts are integers"""
    with pytest.raises(TypeError):
        Fraction(1.5, 2)
    with pytest.raises(TypeError):
        Fraction(1, 2.0)    #2.0 looks whole but is actually a float


def test_init_rejects_non_positive_denominator():
    """checks that negative denominators and 0 denominators are refused"""
    with pytest.raises(ValueError):
        Fraction(1, 0)
    with pytest.raises(ValueError):
        Fraction(1, -2)


def test_attributes_read_only():
    """checks that both the numerator and denominator cannot be changed afterwards"""
    f = Fraction(1, 2)
    with pytest.raises(AttributeError):
        f.numerator = 5

"""comparisons"""

def test_eq_and_ne():
    """checks if 1/2 is the same as 2/4"""
    assert Fraction(1, 2) == Fraction(2, 4)
    assert Fraction(1, 2) != Fraction(1, 3)
    assert not (Fraction(1, 2) != Fraction(2, 4))


def test_ordering():
    """checks <, >, <= and >=, also with negative fractions"""
    assert Fraction(1, 3) < Fraction(1, 2)
    assert Fraction(1, 2) > Fraction(1, 3)
    assert Fraction(1, 2) <= Fraction(2, 4)
    assert Fraction(1, 2) >= Fraction(2, 4)
    assert Fraction(-3, 4) < Fraction(-1, 2)


def test_compare_with_other_type():
    """checks what happens when comparing with a nonfraction"""
    f = Fraction(1, 2)
    assert f.__eq__(0.5) is NotImplemented
    assert (f == 0.5) is False
    with pytest.raises(TypeError):
        f < 0.5

"""the 4 extra methods"""


def test_repr():
    """checks the output that looks like the call"""
    assert repr(Fraction(2, 4)) == "Fraction(1, 2)"


def test_str():
    """checks the easy to read string output"""
    assert str(Fraction(2, 4)) == "1/2"
    assert str(Fraction(-4, 6)) == "-2/3"

def test_add():
    """checks the addition and that the output comes back reduced"""
    assert Fraction(1, 2) + Fraction(1, 3) == Fraction(5, 6)
    assert Fraction(1, 2) + Fraction(1, 2) == Fraction(1, 1)


def test_mul():
    """checks the multiplication and the reduction of the answer"""
    assert Fraction(2, 3) * Fraction(3, 4) == Fraction(1, 2)
    assert Fraction(1, 2) * Fraction(0, 5) == Fraction(0, 1)