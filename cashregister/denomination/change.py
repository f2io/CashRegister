from abc import abstractmethod
from typing import Generic, TypeVar


TDenomination = TypeVar("TDenomination")


class Change(Generic[TDenomination]):
    def __init__(self, value: float, denomination: TDenomination):
        """Abstract class to define generic denomination and convert it to string

        Args:
            value (float): change value
            denomination (TDenomination): generic denomination

        Raises:
            NotImplementedError: require __str__ implementation to convert generic denomination to string
        """
        self.value = value
        self.denomination = denomination

    @abstractmethod
    def recalculate_value(self) -> float:
        """Recalculate the value using current denomination"""
        pass

    @abstractmethod
    def __str__(self):
        """Convert denomination to string"""
        raise NotImplementedError()
