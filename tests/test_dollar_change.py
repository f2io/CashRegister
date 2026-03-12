from cashregister.denomination.dollar.change import DollarDenomination, DollarChange


def test_change_str_greater_than_one():
    change = DollarChange(
        value=1.69,
        denomination=DollarDenomination(dollar=1, quarter=2, nickel=3, penny=4),
    )
    assert str(change) == "1 dollar,2 quarters,3 nickels,4 pennies"

    change = DollarChange(
        value=3.69,
        denomination=DollarDenomination(dollar=3, quarter=2, nickel=3, penny=4),
    )
    assert str(change) == "3 dollars,2 quarters,3 nickels,4 pennies"


def test_change_str_with_none_values():
    change = DollarChange(value=1, denomination=DollarDenomination(dollar=1))
    assert str(change) == "1 dollar"

    change = DollarChange(value=0.50, denomination=DollarDenomination(quarter=2))
    assert str(change) == "2 quarters"

    change = DollarChange(value=0.15, denomination=DollarDenomination(nickel=3))
    assert str(change) == "3 nickels"

    change = DollarChange(value=0.04, denomination=DollarDenomination(penny=4))
    assert str(change) == "4 pennies"
