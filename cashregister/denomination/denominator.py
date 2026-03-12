from abc import abstractmethod
from typing import Generic, TypeVar

from cashregister.denomination.change import Change
from cashregister.denomination.converter import IValueConverter
from cashregister.handler.transaction import Transaction

TOutputChange = TypeVar("TOutputChange", bound=Change)


class Denominator(Generic[TOutputChange]):
    @abstractmethod
    def get_converters(self) -> list[IValueConverter]:
        """Get all converters available to apply the transformation/conversion.

        Returns:
            list[IValueConverter]: list of converters, the execution will based on this order.

        Raises:
            NotImplementedError: require the implementation
        """
        raise NotImplementedError

    @abstractmethod
    def convert_to_change(self, value: float, result: dict[str, int]) -> TOutputChange:
        """Convert the transformation result to a typed change
        Args:
            value[float]: change value.
            result[dict[str,int]]: it is dictionary with convert identifer and denomination value
        Returns:
            TOutputChange: typed change denomination.

        Raises:
            NotImplementedError: require the implementation.
        """
        raise NotImplementedError

    def process(self, tx: Transaction) -> TOutputChange:
        """Process the change denomination through executing the converters in sequence.
        Args:
            tx[Transaction]: object with owed value and paid value.
        Return:
            TOutputChange: type change denomination.
        """
        assert tx.paid > tx.owed, (
            f"Paid: {tx.paid} must be greater than owed: {tx.owed}"
        )

        orig_change = change = round(tx.paid - tx.owed, 2)

        denominator_value = {}
        for converter in self.get_converters():
            (value, change) = converter.convert(round(change, 2))

            denominator = converter.get_identifier()
            if denominator in denominator_value:
                raise ValueError(
                    f"Converters contains duplicated denominator, got: {denominator}::{converter.__class__}"
                )

            if value > 0:
                denominator_value[denominator] = value

            if change == 0:
                # Exit early since there is not remaining value
                break

        return self.convert_to_change(value=orig_change, result=denominator_value)
