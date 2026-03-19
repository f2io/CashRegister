from dataclasses import dataclass, field

from cashregister.denomination.change import Change
from cashregister.denomination.dollar.converter import (
    DimeConverter,
    NickelConverter,
    PennyConverter,
    QuarterConverter,
)


@dataclass
class DollarDenomination:
    dollar: int | None = field(default=None)
    quarter: int | None = field(default=None)
    dime: int | None = field(default=None)
    nickel: int | None = field(default=None)
    penny: int | None = field(default=None)

    def __post_init__(self):
        """Validate denomination values after construction.

        Raises:
            AssertionError: if any denomination is non-positive or all are undefined.

        Note:
            These are safeguards for converter logic — values are produced by converters,
            not user input. A violation indicates a misconfigured converter, not invalid
            user data.
        """
        assert not self.dollar or self.dollar > 0, "dollar needs to be greater than zero"
        assert not self.quarter or self.quarter > 0, "quarter needs to be greater than zero"
        assert not self.dime or self.dime > 0, "dime needs to be greater than zero"
        assert not self.nickel or self.nickel > 0, "nickels needs to be greater than zero"
        assert not self.penny or self.penny > 0, "pennies needs to be greater than zero"

        assert self.dollar or self.quarter or self.dime or self.nickel or self.penny, (
            "one denomination needs to be defined"
        )


class DollarChange(Change[DollarDenomination]):
    def __init__(self, value: float, denomination: DollarDenomination):
        super().__init__(value, denomination)

    def recalculate_value(self) -> float:
        total = 0.0
        total += self.denomination.dollar or 0.0
        total += (self.denomination.quarter or 0.0) * QuarterConverter.QUARTER
        total += (self.denomination.dime or 0.0) * DimeConverter.DIME
        total += (self.denomination.nickel or 0.0) * NickelConverter.NICKEL
        total += (self.denomination.penny or 0.0) * PennyConverter.PENNY
        return round(total, 2)

    def __str__(self):
        components = []

        if self.denomination.dollar is not None and self.denomination.dollar > 0:
            components.append(f"{self.denomination.dollar} dollar{('s' if self.denomination.dollar > 1 else '')}")
        if self.denomination.quarter is not None and self.denomination.quarter > 0:
            components.append(f"{self.denomination.quarter} quarter{('s' if self.denomination.quarter > 1 else '')}")
        if self.denomination.dime is not None and self.denomination.dime > 0:
            components.append(f"{self.denomination.dime} dime{('s' if self.denomination.dime > 1 else '')}")
        if self.denomination.nickel is not None and self.denomination.nickel > 0:
            components.append(f"{self.denomination.nickel} nickel{('s' if self.denomination.nickel > 1 else '')}")
        if self.denomination.penny is not None and self.denomination.penny > 0:
            components.append(f"{self.denomination.penny} {('pennies' if self.denomination.penny > 1 else 'penny')}")

        return ",".join(components)
