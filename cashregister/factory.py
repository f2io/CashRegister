from cashregister.denomination.dollar.denominator import DollarDenominator
from cashregister.denomination.dollar.denominator_shuffle_order import (
    DollarDenominatorWithRandomOrder,
)
from cashregister.handler.dual_denominator import DualDenominatorHandler


class DenominationFactory:
    def __init__(self):
        self.dollar = DollarDenominator()
        self.random_dollar = DollarDenominatorWithRandomOrder()

    def build_dollar_denominator_with_random_case(self) -> DualDenominatorHandler:
        """Create a denominator with dollar descrimination and random selection when owed is divided by 3"""

        return DualDenominatorHandler(
            denominator=self.dollar,
            denominator_owed_divided_by_3=self.random_dollar,
        )


builder = DenominationFactory()
