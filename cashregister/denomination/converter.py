from abc import abstractmethod
from typing import Tuple


class IValueConverter:
    @abstractmethod
    def get_identifier(self) -> str:
        """Get the identifier which is related to the conversion

        Raises:
            NotImplementedError: require the implementation

        Returns:
            str: the identifier of conversion
        """
        raise NotImplementedError

    @abstractmethod
    def convert(self, value: float) -> Tuple[int, float]:  # denomination value and remaining
        """Convert change value to a denomination

        Args:
            value (float): change value

        Raises:
            NotImplementedError: require the implementation

        Returns:
            Tuple[int, float]: denomination value and remaining
        """
        raise NotImplementedError()
