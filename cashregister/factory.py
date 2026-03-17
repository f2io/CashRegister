from cashregister.denomination.dollar.denominator import DollarDenominator
from cashregister.denomination.dollar.denominator_shuffle_order import (
    DollarDenominatorWithRandomOrder,
)
from cashregister.handler.filesystem_denominator import (
    DivThreeDenominatorSelector,
    AutoSelectionDenominatorHandler,
)


class DenominationFactory:
    def __init__(self):
        self.dollar = DollarDenominator()
        self.random_dollar = DollarDenominatorWithRandomOrder()

    def create_dollar_denominator_with_random_case(
        self,
    ) -> AutoSelectionDenominatorHandler:
        """Create a denominator with dollar discrimination and random selection when owed is divided by 3"""
        selector = DivThreeDenominatorSelector(
            denominator=self.dollar,
            denominator_owed_divided_by_3=self.random_dollar,
        )
        return AutoSelectionDenominatorHandler(selector=selector)


creator = DenominationFactory()
