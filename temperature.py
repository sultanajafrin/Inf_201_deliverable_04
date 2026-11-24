class Temperature:
    """Temparatue in three different units Celsius (C), Fahrenheit (F) or Kelvin (K)."""

    # The lowest possible value in each unit.
    ABSOLUTE_ZERO = {"C": -273.15, "F": -459.67, "K": 0}

    # Two temparatures closer than this are treated as equal.
    TOLERANCE = 1e-9

    def __init__(self, value: float, unit: str = "C") -> None:
        """Makes a temperature. Gives a ValueError if the unit is wrong or it is below absolute zero."""
        unit = unit.upper()
        if unit not in self.ABSOLUTE_ZERO:
            raise ValueError(f"Invalid unit: {unit}")
        if value < self.ABSOLUTE_ZERO[unit] - self.TOLERANCE:
            raise ValueError(f"Temperature is below absolute zero: {value} {unit}")
        self._value = value
        self._unit = unit

    @property
    def value(self) -> float:
        """Returns the value. It can be read but not changed."""
        return self._value

    @property
    def unit(self) -> str:
        """Returns the unit. It can be read but not changed."""
        return self._unit

    def to_celsius(self) -> float:
        """Returns the temperature in Celsius."""
        if self._unit == "C":
            return self._value
        if self._unit == "K":
            return self._value - 273.15
        return (self._value - 32) * 5 / 9

    def to_fahrenheit(self) -> float:
        """Returns the temperature in Fahrenheit."""
        if self._unit == "F":
            return self._value
        if self._unit == "C":
            return self._value * 9 / 5 + 32
        return (self._value - 273.15) * 9 / 5 + 32

    def to_kelvin(self) -> float:
        """Returns the temperature in Kelvin."""
        if self._unit == "K":
            return self._value
        if self._unit == "C":
            return self._value + 273.15
        return (self._value - 32) * 5 / 9 + 273.15

    def convert_to(self, target_unit: str) -> "Temperature":
        """Returns a new Temperature in the unit we ask for."""
        target_unit = target_unit.upper()
        if target_unit == "C":
            return Temperature(self.to_celsius(), "C")
        if target_unit == "F":
            return Temperature(self.to_fahrenheit(), "F")
        if target_unit == "K":
            return Temperature(self.to_kelvin(), "K")
        raise ValueError(f"Invalid unit: {target_unit}")

    def __repr__(self) -> str:
        """Returns a clear text like Temperature(25.0, 'C')."""
        return f"Temperature({float(self._value)!r}, {self._unit!r})"

    def __str__(self) -> str:
        """Returns a readable text like 25.00 °C."""
        if self._unit == "K":
            return f"{self._value:.2f} K"
        return f"{self._value:.2f} °{self._unit}"

    # For the comparisons we change both temparatures to Kelvin first,
    # so that different units can be compared.

    def __eq__(self, other: object) -> bool:
        """Returns True if the two temperatures are equal."""
        if not isinstance(other, Temperature):
            return NotImplemented
        return abs(self.to_kelvin() - other.to_kelvin()) <= self.TOLERANCE

    def __ne__(self, other: object) -> bool:
        """Returns True if the two temperatures are not equal."""
        result = self.__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        return not result

    def __lt__(self, other: "Temperature") -> bool:
        """Returns True if this temperature is lower than the other."""
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() < other.to_kelvin() - self.TOLERANCE

    def __le__(self, other: "Temperature") -> bool:
        """Returns True if this temperature is lower than or equal to the other."""
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() <= other.to_kelvin() + self.TOLERANCE

    def __gt__(self, other: "Temperature") -> bool:
        """Returns True if this temperature is higher than the other."""
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() > other.to_kelvin() + self.TOLERANCE

    def __ge__(self, other: "Temperature") -> bool:
        """Returns True if this temperature is higher than or equal to the other."""
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() >= other.to_kelvin() - self.TOLERANCE