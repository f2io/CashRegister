import logging

from cashregister.denomination.denominator import Denominator
from cashregister.exceptions.exception import (
    CashRegisteExceptionGroup,
    CashRegisterError,
)
from cashregister.stream.filesystem import PipelineTransactionFile
from cashregister.handler.transaction import Transaction
from cashregister.util.division import Division

logger = logging.getLogger(__name__)


class DualDenominatorHandler:
    """
    Handler responsible to apply random denomination if the owed value is divided by 3.
    Using FileSytem as input and output.
    """

    def __init__(
        self,
        denominator: Denominator,
        denominator_owed_divided_by_3: Denominator,
    ):
        self.denominator = denominator
        self.random_denominator = denominator_owed_divided_by_3

    def get_denominator(self, tx: Transaction) -> Denominator:
        """Denominator handler based on transaction rule"""
        if Division.is_divided_by(tx.owed):
            return self.random_denominator

        return self.denominator

    def run(self, input: str, output: str):
        """
        Args:
            input[str]: filename with transaction
        """
        with PipelineTransactionFile(input=input, output=output) as pipeline:
            try:
                tx = pipeline.read()
                while tx:
                    denominator = self.get_denominator(tx)
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
                raise CashRegisteExceptionGroup(exc_info, [exc])

            except Exception as exc:
                info = pipeline.get_info()

                # In case is using OTEL to export log
                logger.error(f"Error({info}): {str(exc)}", exc_info=exc)

                # Propagate unknown
                raise
