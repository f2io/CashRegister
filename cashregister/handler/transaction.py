from dataclasses import dataclass, field
from typing import Self


@dataclass
class Transaction:
    owed: float = field()
    paid: float = field()
    change: float = field(init=False)

    def __post_init__(self):
        assert self.owed >= 0, "owed must be non-negative"
        assert self.paid >= 0, "paid must be non-negative"
        assert self.paid > self.owed, "paid must be greater than owed"

        self.change = round(self.paid - self.owed, 2)

    def __str__(self) -> str:
        return f"transaction(owed={self.owed}, paid={self.paid}, change={self.change})"

    @classmethod
    def from_string(cls, owed: str, paid: str) -> Self:
        """ "
        creates a Transaction object from string values of owed and paid
        args:
            owed: string representation of the amount owed
            paid: string representation of the amount paid
        returns:
            Transaction object with owed and paid as floats
        """
        float_owed = float(owed)
        float_paid = float(paid)

        return cls(float_owed, float_paid)
