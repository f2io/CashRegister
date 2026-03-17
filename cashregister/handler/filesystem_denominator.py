import logging

from cashregister.denomination.denominator import Denominator
from cashregister.exceptions.exception import (
    CashRegisterExceptionGroup,
    CashRegisterError,
)
from cashregister.denomination.denominator_selector import IDenominatorSelector
from cashregister.handler.transaction import Transaction
from cashregister.stream.filesystem import PipelineTransactionFile
from cashregister.util.division import Division

logger = logging.getLogger(__name__)


class DivThreeDenominatorSelector(IDenominatorSelector[Transaction]):
    """Selects the random denominator when owed is divisible by 3."""

    def __init__(
        self,
        denominator: Denominator,
        denominator_owed_divided_by_3: Denominator,
    ):
        self.denominator = denominator
        self.random_denominator = denominator_owed_divided_by_3

    def select(self, tx: Transaction) -> Denominator:
        if Division.is_divided_by(tx.owed):
            return self.random_denominator

        return self.denominator


class AutoSelectionDenominatorHandler:
    """
    Handler responsible to apply denomination based on selector strategy.
    Using FileSytem as input and output.
    """

    def __init__(self, selector: IDenominatorSelector):
        self.selector = selector

    def run(self, input: str, output: str):
        """
        Args:
            input[str]: filename with transaction
        """
        with PipelineTransactionFile(input=input, output=output) as pipeline:
            try:
                tx = pipeline.read()
                while tx:
                    denominator = self.selector.select(tx)
                    logger.info(
                        f"[selection] denominator={type(denominator)}, tx={str(tx)}"
                    )

                    change = denominator.process(tx)
                    pipeline.write(change)

                    # Next
                    tx = pipeline.read()
            except CashRegisterError as exc:
                info = pipeline.get_info()
                exc_info = f"{info}: {str(exc)}"

                # Propagate/Enrich known-error
                raise CashRegisterExceptionGroup(exc_info, [exc])

            except Exception as exc:
                info = pipeline.get_info()

                # In case is using OTEL to export log
                logger.error(f"Error({info}): {str(exc)}", exc_info=exc)

                # Propagate unknown
                raise
