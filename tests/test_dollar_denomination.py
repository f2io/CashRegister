from cashregister.denomination.dollar.denominator import DollarDenominator
from cashregister.denomination.dollar.denominator_shuffle_order import (
    DollarDenominatorWithRandomOrder,
)
from cashregister.handler.transaction import Transaction


def test_dollar_denomination_case1():
    denomination = DollarDenominator()
    transaction = Transaction(owed=2.12, paid=3.00)

    result = denomination.process(tx=transaction)

    assert result.denomination.dollar is None, f"got: {result.denomination.dollar}"
    assert result.denomination.quarter == 3, f"got: {result.denomination.quarter}"
    assert result.denomination.dime == 1, f"got: {result.denomination.dime}"
    assert result.denomination.nickel is None, f"got: {result.denomination.nickel}"
    assert result.denomination.penny == 3, f"got: {result.denomination.penny}"


def test_dollar_denomination_case2():
    denomination = DollarDenominator()
    transaction = Transaction(owed=1.97, paid=2.00)

    result = denomination.process(tx=transaction)

    assert result.denomination.dollar is None, f"got: {result.denomination.dollar}"
    assert result.denomination.quarter is None, f"got: {result.denomination.quarter}"
    assert result.denomination.dime is None, f"got: {result.denomination.dime}"
    assert result.denomination.nickel is None, f"got: {result.denomination.nickel}"
    assert result.denomination.penny == 3, f"got: {result.denomination.penny}"


def test_dollar_denomination_case3():
    denomination = DollarDenominator()
    transaction = Transaction(owed=3.33, paid=5.00)

    result = denomination.process(tx=transaction)

    assert result.denomination.dollar == 1, f"got: {result.denomination.dollar}"
    assert result.denomination.quarter == 2, f"got: {result.denomination.quarter}"
    assert result.denomination.dime == 1, f"got: {result.denomination.dime}"
    assert result.denomination.nickel == 1, f"got: {result.denomination.nickel}"
    assert result.denomination.penny == 2, f"got: {result.denomination.penny}"


def test_dollar_denomination_random_order():
    denomination = DollarDenominatorWithRandomOrder()
    transaction = Transaction(owed=3.33, paid=5.00)

    result = denomination.process(tx=transaction)

    assert result.value == result.recalculate_value()


def test_dollar_denomination_random_order_with_all_converters_disabled():
    denomination = DollarDenominatorWithRandomOrder(
        get_random_converters=lambda converters: [False] * len(converters)
    )
    transaction = Transaction(owed=3.33, paid=5.00)

    result = denomination.process(tx=transaction)

    assert result.denomination.penny == 167
    assert result.value == result.recalculate_value()
