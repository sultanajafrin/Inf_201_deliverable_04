import math


class Fraction:
    """a fraction that is reduced and has a positive denominator"""

    def __init__(self, numerator: int, denominator: int = 1) -> None:
        """Raises TypeError if not integers, ValueError if denominator <= 0."""
        if type(numerator) is not int or type(denominator) is not int:
            raise TypeError("the numerator and denominator must be integers")

        #the task says strictly so it cant be 0
        if denominator <= 0:
            raise ValueError("the denominator must be strictly positive")

        #we reduce immidiately to make equal values stored the same. this will make future taks easier
        divisor = math.gcd(numerator, denominator)
        self._numerator = numerator // divisor
        self._denominator = denominator // divisor

    @property
    def numerator(self) -> int:
        """Read-only numerator."""
        return self._numerator

    @property
    def denominator(self) -> int:
        """Read-only denominator."""
        return self._denominator

    """these are the six required comparisons
    we use cross multiplication to get solutions, this works because the denominators are always positive"""

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Fraction):
            return NotImplemented              #an error message if wrong types
        return (self._numerator == other._numerator       #both fractions are reduced, so can simply compare
                and self._denominator == other._denominator)

    #uses eq, but opposite
    def __ne__(self, other: object) -> bool:
        result = self.__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        return not result

    #checks less than
    def __lt__(self, other: "Fraction") -> bool:
        if not isinstance(other, Fraction):
            return NotImplemented
        return (self._numerator * other._denominator
                < other._numerator * self._denominator)

    #same as last one but includes equal
    def __le__(self, other: "Fraction") -> bool:
        if not isinstance(other, Fraction):
            return NotImplemented
        return (self._numerator * other._denominator
                <= other._numerator * self._denominator)

    #other direction, but same
    def __gt__(self, other: "Fraction") -> bool:
        if not isinstance(other, Fraction):
            return NotImplemented
        return (self._numerator * other._denominator
                > other._numerator * self._denominator)

    # add equal again
    def __ge__(self, other: "Fraction") -> bool:
        if not isinstance(other, Fraction):
            return NotImplemented
        return (self._numerator * other._denominator
                >= other._numerator * self._denominator)

    """ the four extra methods: repr, str, add and mul"""

    #gives output that looks like the call that created the object
    def __repr__(self) -> str:
        return f"Fraction({self._numerator}, {self._denominator})"

    #looks better for the reader and gives a readable version of the fraction
    def __str__(self) -> str:
        return f"{self._numerator}/{self._denominator}"

    def __add__(self, other: "Fraction") -> "Fraction":
        if not isinstance(other, Fraction):
            return NotImplemented
        return Fraction(         #we use fraction again so it gets reduced at the end of the calculation
            self._numerator * other._denominator
            + other._numerator * self._denominator,
            self._denominator * other._denominator,
        )

    #this one is simple as it multiplies straight across and then reduces at the end because of fraction
    def __mul__(self, other: "Fraction") -> "Fraction":
        if not isinstance(other, Fraction):
            return NotImplemented
        return Fraction(
            self._numerator * other._numerator,
            self._denominator * other._denominator,
        )