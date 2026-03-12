import random
import logging
from typing import Callable
from cashregister.denomination.converter import IValueConverter
from cashregister.denomination.dollar.denominator import DollarDenominator
from cashregister.denomination.dollar.converter import (
    standard_dollar_converters,
    PennyConverter,
)


logger = logging.getLogger(__name__)


class DollarDenominatorWithRandomOrder(DollarDenominator):
    def __init__(
        self,
        converters: list[IValueConverter] = standard_dollar_converters,
        get_random_converters: Callable[[list[IValueConverter]], list[bool]]
        | None = None,
    ) -> None:
        """Dollar denomination with random denomination

        Args:
            converters (list[IValueConverter], optional): list of converters. Defaults to dollar_converters.
            get_random_converters (Callable[[list[IValueConverter]], list[bool]] | None, optional): delegate lambda to return a list of enabled converters. Defaults to calculate random weights 50%/50%.

        """
        super().__init__(converters)

        assert any(
            [isinstance(converter, PennyConverter) for converter in converters]
        ), "Expected to have PennyConverter available"

        self._get_random_converters = get_random_converters or (
            lambda converters: random.choices(
                [True, False], weights=[50, 50], k=len(converters)
            )
        )

    def get_converters(self) -> list[IValueConverter]:
        """Disable random converter, so denomination could be just Quarters and Pennies, or another combination

        Returns:
            list[ValueConverter]: return random converters to define denomination

        Note:
            Except Penny converter is not removed so it can work as a safeguard in case all converters are removed.
        """

        enabled_converter = self._get_random_converters(self.converters)

        assert len(enabled_converter) == len(self.converters), (
            "List of enabled converters must have the same size of converters"
        )

        random_converters = [
            converter
            for (converter, enabled) in zip(self.converters, enabled_converter)
            if enabled or isinstance(converter, PennyConverter)
        ]

        logger.info(random_converters)
        return random_converters
