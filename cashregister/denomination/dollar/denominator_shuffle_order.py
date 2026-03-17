import random
import logging
from typing import Callable

from cashregister.denomination.converter import IValueConverter
from cashregister.denomination.denominator import Denominator
from cashregister.denomination.dollar.change import DollarChange, DollarDenomination
from cashregister.denomination.dollar.converter import (
    standard_dollar_converters,
    PennyConverter,
)


logger = logging.getLogger(__name__)


class DollarDenominatorWithRandomOrder(Denominator[DollarChange]):
    def __init__(
        self,
        converters: list[IValueConverter] = standard_dollar_converters,
        safeguard_converter: type[IValueConverter] = PennyConverter,
        get_random_converters: Callable[[list[IValueConverter]], list[bool]]
        | None = None,
    ) -> None:
        """Dollar denomination with random denomination order.

        Args:
            converters (list[IValueConverter], optional): list of converters. Defaults to standard_dollar_converters.
            safeguard_converter (type[IValueConverter], optional): converter type always kept active regardless of random selection. Defaults to PennyConverter.
            get_random_converters (Callable[[list[IValueConverter]], list[bool]] | None, optional): delegate lambda to return a list of enabled converters. Defaults to 50%/50% random weights.
        """
        assert len(converters) > 0, "At least one converter must be provided"
        assert any(isinstance(c, safeguard_converter) for c in converters), (
            f"Expected safeguard converter '{safeguard_converter.__name__}' in converters"
        )

        self.converters = converters
        self._safeguard_type = safeguard_converter
        self._get_random_converters = get_random_converters or (
            lambda converters: random.choices(
                [True, False], weights=[50, 50], k=len(converters)
            )
        )

    def get_converters(self) -> list[IValueConverter]:
        """Return converters with random enabling, always keeping the safeguard converter.

        Returns:
            list[IValueConverter]: active converters for this denomination round.

        Note:
            The safeguard converter is never removed so it handles any remaining change
            when all other converters are randomly disabled.
        """
        enabled_converter = self._get_random_converters(self.converters)

        assert len(enabled_converter) == len(self.converters), (
            "List of enabled converters must have the same size of converters"
        )

        random_converters = [
            converter
            for (converter, enabled) in zip(self.converters, enabled_converter)
            if enabled or isinstance(converter, self._safeguard_type)
        ]

        logger.info(random_converters)
        return random_converters

    def convert_to_change(self, value: float, result: dict[str, int]) -> DollarChange:
        return DollarChange(value=value, denomination=DollarDenomination(**result))
