from abc import abstractmethod
from typing import Generic, TypeVar

from cashregister.denomination.denominator import Denominator

TInput = TypeVar("TInput")


class IDenominatorSelector(Generic[TInput]):
    @abstractmethod
    def select(self, tx: TInput) -> Denominator:
        """Select the appropriate denominator for a given transaction.

        Args:
            tx (Transaction): the transaction to evaluate.

        Returns:
            Denominator: the denominator to apply.

        Raises:
            NotImplementedError: require the implementation.
        """
        raise NotImplementedError()
