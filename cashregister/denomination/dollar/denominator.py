from cashregister.denomination.converter import IValueConverter
from cashregister.denomination.denominator import Denominator
from cashregister.denomination.dollar.change import DollarChange, DollarDenomination
from cashregister.denomination.dollar.converter import (
    standard_dollar_converters,
)


class DollarDenominator(Denominator[DollarChange]):
    def __init__(self, converters: list[IValueConverter] = standard_dollar_converters) -> None:
        """Dollar Denomination using standard converters(quarter, dime, ...)

        Args:
            converters (list[IValueConverter], optional): list of converters. Defaults to standard_dollar_converters.
        """
        self.converters: list[IValueConverter] = converters

    def get_converters(self) -> list[IValueConverter]:
        """Get all converters available

        Returns:
            list[IValueConverter]: list of converters
        """
        return self.converters

    def convert_to_change(self, value: float, result: dict[str, int]) -> DollarChange:
        """Convert to type dollar change

        Args:
            value (float): change value
            result (dict[str, int]): dictionary of converter identifier and denomination value

        Returns:
            DollarChange: typed dollar change which has all denominations
        """
        return DollarChange(value=value, denomination=DollarDenomination(**result))
