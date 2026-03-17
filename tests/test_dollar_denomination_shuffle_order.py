import pytest
from cashregister.denomination.dollar.denominator_shuffle_order import (
    DollarDenominatorWithRandomOrder,
)
from cashregister.denomination.converter import IValueConverter
from cashregister.denomination.dollar.converter import (
    DollarConverter,
    QuarterConverter,
    PennyConverter,
)
from cashregister.handler.transaction import Transaction


# --- Constructor guard: safeguard_converter not in converters ---


def test_init_raises_when_safeguard_converter_not_in_converters():
    converters: list[IValueConverter] = [DollarConverter(), QuarterConverter()]
    with pytest.raises(AssertionError):
        DollarDenominatorWithRandomOrder(converters=converters)


# --- get_converters guard: mismatched length from get_random_converters ---


def test_get_converters_raises_on_mismatched_length():
    denomination = DollarDenominatorWithRandomOrder(
        get_random_converters=lambda converters: [True]  # wrong length
    )
    transaction = Transaction(owed=1.00, paid=2.00)
    with pytest.raises(AssertionError):
        denomination.process(tx=transaction)


# --- All converters enabled ---


def test_all_converters_enabled_matches_standard_denominator():
    denomination = DollarDenominatorWithRandomOrder(
        get_random_converters=lambda converters: [True] * len(converters)
    )
    transaction = Transaction(owed=1.00, paid=2.41)

    result = denomination.process(tx=transaction)

    assert result.denomination.dollar == 1
    assert result.denomination.quarter == 1
    assert result.denomination.dime == 1
    assert result.denomination.nickel == 1
    assert result.denomination.penny == 1
    assert result.value == result.recalculate_value()
    assert str(result) == ("1 dollar,1 quarter,1 dime,1 nickel,1 penny")


def test_all_converters_enabled_plural_strings():
    denomination = DollarDenominatorWithRandomOrder(
        get_random_converters=lambda converters: [True] * len(converters)
    )
    transaction = Transaction(owed=0.48, paid=3.00)

    result = denomination.process(tx=transaction)

    assert result.denomination.dollar == 2
    assert result.denomination.quarter == 2
    assert result.denomination.dime is None
    assert result.denomination.nickel is None
    assert result.denomination.penny == 2
    assert result.value == result.recalculate_value()
    assert str(result) == "2 dollars,2 quarters,2 pennies"


def test_plural_dimes_and_pennies():
    denomination = DollarDenominatorWithRandomOrder(
        get_random_converters=lambda converters: [True] * len(converters)
    )
    transaction = Transaction(owed=0.78, paid=1.00)

    result = denomination.process(tx=transaction)

    assert result.denomination.dollar is None
    assert result.denomination.quarter is None
    assert result.denomination.dime == 2
    assert result.denomination.nickel is None
    assert result.denomination.penny == 2
    assert result.value == result.recalculate_value()
    assert str(result) == "2 dimes,2 pennies"


def test_plural_nickels_and_pennies():
    # Disable dimes so nickels absorb the remainder
    denomination = DollarDenominatorWithRandomOrder(
        get_random_converters=lambda converters: [True, True, False, True, True]
    )
    transaction = Transaction(owed=0.88, paid=1.00)

    result = denomination.process(tx=transaction)

    assert result.denomination.dollar is None
    assert result.denomination.quarter is None
    assert result.denomination.dime is None
    assert result.denomination.nickel == 2
    assert result.denomination.penny == 2
    assert result.value == result.recalculate_value()
    assert str(result) == "2 nickels,2 pennies"


# --- Partial/selective enabling ---


def test_partial_converters_only_quarters_and_pennies():
    # Enable only dollar=False, quarter=True, dime=False, nickel=False, penny=True
    denomination = DollarDenominatorWithRandomOrder(
        get_random_converters=lambda converters: [False, True, False, False, True]
    )
    transaction = Transaction(owed=3.33, paid=5.00)

    result = denomination.process(tx=transaction)

    assert result.denomination.dollar is None
    assert result.denomination.quarter == 6
    assert result.denomination.dime is None
    assert result.denomination.nickel is None
    assert result.denomination.penny == 17
    assert result.value == result.recalculate_value()
    assert str(result) == "6 quarters,17 pennies"


# --- Custom converters list ---


def test_custom_converters_list():
    converters: list[IValueConverter] = [QuarterConverter(), PennyConverter()]
    denomination = DollarDenominatorWithRandomOrder(
        converters=converters,
        get_random_converters=lambda converters: [True] * len(converters),
    )
    transaction = Transaction(owed=0.50, paid=1.00)

    result = denomination.process(tx=transaction)

    assert result.denomination.quarter == 2
    assert result.denomination.penny is None
    assert result.value == result.recalculate_value()
