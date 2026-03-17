from dataclasses import dataclass, field
from typing import Self

from cashregister.exceptions.parser import (
    InvalidFieldTypeTransactionError,
    InvalidEntryTransactionError,
)


@dataclass
class Transaction:
    owed: float = field()
    paid: float = field()
    change: float = field(init=False)

    def __post_init__(self):
        """Validate transaction values after construction.

        Raises:
            InvalidEntryTransactionError: if owed or paid are negative, or paid does not exceed owed.
        """
        if self.owed < 0:
            raise InvalidEntryTransactionError("owed must be non-negative")
        if self.paid < 0:
            raise InvalidEntryTransactionError("paid must be non-negative")
        if self.paid <= self.owed:
            raise InvalidEntryTransactionError("paid must be greater than owed")

        self.change = round(self.paid - self.owed, 2)

    def __str__(self) -> str:
        return f"transaction(owed={self.owed}, paid={self.paid}, change={self.change})"

    @classmethod
    def from_string(cls, owed: str, paid: str) -> Self:
        """creates a Transaction object from string values of owed and paid

        args:
            owed: string representation of the amount owed
            paid: string representation of the amount paid

        returns:
            Transaction: object with owed and paid as floats
        """
        try:
            float_owed = float(owed)
            float_paid = float(paid)
        except ValueError as exc:
            # Error handler
            raise InvalidFieldTypeTransactionError(
                f"Expected float values, got owed={owed}, paid={paid}, error:{str(exc)}"
            )

        return cls(float_owed, float_paid)
