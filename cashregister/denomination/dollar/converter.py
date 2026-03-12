from typing import Tuple

from cashregister.denomination.converter import IValueConverter


class DollarConverter(IValueConverter):
    DOLLAR = 1.00

    def get_identifier(self):
        return "dollar"

    def convert(self, value: float) -> Tuple[int, float]:
        denomination = int(value / DollarConverter.DOLLAR)
        remaining = value % DollarConverter.DOLLAR
        return (denomination, remaining)


class QuarterConverter(IValueConverter):
    QUARTER = 0.25

    def get_identifier(self):
        return "quarter"

    def convert(self, value: float) -> Tuple[int, float]:
        denomination = int(value / QuarterConverter.QUARTER)
        remaining = value % QuarterConverter.QUARTER
        return (denomination, remaining)


class DimeConverter(IValueConverter):
    DIME = 0.10

    def get_identifier(self):
        return "dime"

    def convert(self, value: float) -> Tuple[int, float]:
        denomination = int(value / DimeConverter.DIME)
        remaining = value % DimeConverter.DIME
        return (denomination, remaining)


class NickelConverter(IValueConverter):
    NICKEL = 0.05

    def get_identifier(self):
        return "nickel"

    def convert(self, value: float) -> Tuple[int, float]:
        denomination = int(value / NickelConverter.NICKEL)
        remaining = value % NickelConverter.NICKEL
        return (denomination, remaining)


class PennyConverter(IValueConverter):
    PENNY = 0.01

    def get_identifier(self):
        return "penny"

    def convert(self, value: float) -> Tuple[int, float]:
        denomination = int(value / PennyConverter.PENNY)
        remaining = value % PennyConverter.PENNY
        return (denomination, remaining)


standard_dollar_converters: list[IValueConverter] = [
    DollarConverter(),
    QuarterConverter(),
    DimeConverter(),
    NickelConverter(),
    PennyConverter(),
]
