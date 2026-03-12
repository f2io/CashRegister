from abc import abstractmethod
from typing import Generic, TypeVar

from cashregister.denomination.change import Change
from cashregister.handler.transaction import Transaction


TInput = TypeVar("TInput", bound=Transaction)
TOutput = TypeVar("TOutput", bound=Change)


class IPipelineInfo:
    @abstractmethod
    def get_info(self) -> str:
        """Return status about pipeline"""
        pass


class IPipeline(Generic[TInput, TOutput]):
    """Pipeline is a interface to declare the bridge types expected for input and output."""

    @abstractmethod
    def read(self) -> TInput | None:
        """Decode input source to a specific type

        Returns:
            TInput: generic type
        """
        raise NotImplementedError()

    @abstractmethod
    def write(self, output: TOutput):
        """Encode output to a specific type

        Args:
            output[TOutput]: generic type
        """

        raise NotImplementedError()
