import pytest
from temperature import Temperature


# (celsius, fahrenheit, kelvin)
REFERENCE_POINTS = [
    (-273.15, -459.67, 0),     # absolute zero
    (-40, -40, 233.15),        # C and F are the same here
    (0, 32, 273.15),           # water freezes
    (37, 98.6, 310.15),        # body temperature
    (100, 212, 373.15),        # water boils
]


# Initialization

def test_default_unit():
    """Tests that the unit is Celsius if we do not give one."""
    t = Temperature(25)
    assert t.unit == "C"


def test_unit_case_insensitive():
    """Tests that a small letter like "c" works and is saved as "C"."""
    t = Temperature(25, "c")
    assert t.unit == "C"


def test_value_and_unit_read_only():
    """Tests that value and unit cannot be changed."""
    t = Temperature(25, "C")
    with pytest.raises(AttributeError):
        t.value = 30
    with pytest.raises(AttributeError):
        t.unit = "F"


# Validation

def test_invalid_unit_raises():
    """Tests that a wrong unit gives a ValueError."""
    with pytest.raises(ValueError):
        Temperature(25, "X")


@pytest.mark.parametrize("value, unit", [
    (-273.16, "C"),
    (-459.68, "F"),
    (-0.01, "K"),
])
def test_below_absolute_zero_raises(value, unit):
    """Tests that a value below absolute zero gives a ValueError."""
    with pytest.raises(ValueError):
        Temperature(value, unit)


# Conversions

@pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
def test_to_celsius(c, f, k):
    """Tests to_celsius when we start in C, F and K."""
    assert Temperature(c, "C").to_celsius() == pytest.approx(c)
    assert Temperature(f, "F").to_celsius() == pytest.approx(c)
    assert Temperature(k, "K").to_celsius() == pytest.approx(c)


@pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
def test_to_fahrenheit(c, f, k):
    """Tests to_fahrenheit when we start in C, F and K."""
    assert Temperature(c, "C").to_fahrenheit() == pytest.approx(f)
    assert Temperature(f, "F").to_fahrenheit() == pytest.approx(f)
    assert Temperature(k, "K").to_fahrenheit() == pytest.approx(f)


@pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
def test_to_kelvin(c, f, k):
    """Tests to_kelvin when we start in C, F and K."""
    assert Temperature(c, "C").to_kelvin() == pytest.approx(k)
    assert Temperature(f, "F").to_kelvin() == pytest.approx(k)
    assert Temperature(k, "K").to_kelvin() == pytest.approx(k)


@pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
def test_convert_to(c, f, k):
    """Tests that convert_to gives the right value and unit."""
    t = Temperature(c, "C")
    assert t.convert_to("F").value == pytest.approx(f)
    assert t.convert_to("k").value == pytest.approx(k)   # small letter works too
    assert t.convert_to("k").unit == "K"


def test_convert_to_invalid_unit_raises():
    """Tests that convert_to gives a ValueError for a wrong unit."""
    with pytest.raises(ValueError):
        Temperature(25, "C").convert_to("X")


def test_convert_to_returns_new_object():
    """Tests that convert_to gives a new object and the original stays the same."""
    original = Temperature(100, "C")
    converted = original.convert_to("F")
    assert converted is not original
    assert original.unit == "C"


# Round trip

@pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
def test_round_trip(c, f, k):
    """Tests that C -> F -> K -> C gives back the temperature we started with."""
    start = Temperature(c, "C")
    back = start.convert_to("F").convert_to("K").convert_to("C")
    assert back == start


# Comparisons

@pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
def test_equal_across_units(c, f, k):
    """Tests that the same temperature in different units is equal."""
    assert Temperature(c, "C") == Temperature(f, "F")
    assert Temperature(f, "F") == Temperature(k, "K")


def test_not_equal():
    """Tests that different temperatures are not equal."""
    assert Temperature(0, "C") != Temperature(33, "F")
    assert Temperature(0, "C") != Temperature(0, "K")    
# 0 C is not 0 K


def test_ordering_across_units():
    """Tests <, <=, > and >= with different units."""
    cold = Temperature(0, "C")
    warm = Temperature(100, "F")
    hot = Temperature(400, "K")
    assert cold < warm < hot
    assert hot > warm > cold
    assert cold <= warm
    assert hot >= warm
    assert cold <= Temperature(32, "F")     
    assert cold >= Temperature(32, "F")     
    assert not cold < Temperature(32, "F")
    assert not cold > Temperature(32, "F")


def test_tolerance():
    """Tests that a very small difference (less than 1e-9) counts as equal."""
    assert Temperature(0, "C") == Temperature(1e-10, "C")
    assert Temperature(0, "C") != Temperature(1e-6, "C")


def test_compare_with_other_type():
    """Tests that comparing with a number gives NotImplemented."""
    t = Temperature(0, "C")
    assert t.__eq__(5) is NotImplemented
    assert t.__lt__(5) is NotImplemented
    assert (t == 5) is False
    with pytest.raises(TypeError):
        t < 5


# Formatting

@pytest.mark.parametrize("value, unit, expected", [
    (25, "C", "Temperature(25.0, 'C')"),
    (98.6, "f", "Temperature(98.6, 'F')"),
    (0, "k", "Temperature(0.0, 'K')"),
])
def test_repr(value, unit, expected):
    """Tests the text we get from repr()."""
    assert repr(Temperature(value, unit)) == expected


@pytest.mark.parametrize("value, unit, expected", [
    (25, "C", "25.00 °C"),
    (98.6, "F", "98.60 °F"),
    (0, "K", "0.00 K"),
])
def test_str(value, unit, expected):
    """Tests the text we get from str()."""
    assert str(Temperature(value, unit)) == expected