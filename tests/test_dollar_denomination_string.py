from cashregister.denomination.dollar.denominator import DollarDenominator
from cashregister.denomination.dollar.denominator_shuffle_order import (
    DollarDenominatorWithRandomOrder,
)
from cashregister.handler.transaction import Transaction


def test_dollar_denomination_case1():
    denomination = DollarDenominator()
    transaction = Transaction(owed=2.12, paid=3.00)

    result = denomination.process(tx=transaction)

    assert str(result) == "3 quarters,1 dime,3 pennies"


def test_dollar_denomination_case2():
    denomination = DollarDenominator()
    transaction = Transaction(owed=1.97, paid=2.00)

    result = denomination.process(tx=transaction)

    assert str(result) == "3 pennies"


def test_dollar_denomination_case3():
    denomination = DollarDenominator()
    transaction = Transaction(owed=3.33, paid=5.00)

    result = denomination.process(tx=transaction)

    assert str(result) == "1 dollar,2 quarters,1 dime,1 nickel,2 pennies"


def test_dollar_denomination_random_order_with_all_converters_disabled():
    denomination = DollarDenominatorWithRandomOrder(
        get_random_converters=lambda converters: [False] * len(converters)
    )
    transaction = Transaction(owed=3.33, paid=5.00)

    result = denomination.process(tx=transaction)

    assert str(result) == "167 pennies"
