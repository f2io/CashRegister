import logging

from cashregister.denomination.denominator import Denominator
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
        # self.dollar = DollarDenominator()
        # self.random_dollar = DollarDenominatorWithRandomOrder()
        self.dollar = denominator
        self.random_dollar = denominator_owed_divided_by_3

    def get_denominator(self, tx: Transaction) -> Denominator:
        """Denominator handler based on transaction rule"""
        if Division.is_divided_by(tx.owed):
            return self.random_dollar

        return self.dollar

    def run(self, input: str, output: str):
        """
        Args:
            input[str]: filename with transaction
        """
        with PipelineTransactionFile(input=input, output=output) as pipeline:
            tx = pipeline.read()
            try:
                while tx:
                    denominator = self.get_denominator(tx)
                    logger.info(
                        f"[selection] denominator={type(denominator)}, tx={str(tx)}"
                    )

                    change = denominator.process(tx)
                    pipeline.write(change)

                    # Next
                    tx = pipeline.read()

            except Exception as exc:
                logger.error(f"Error({pipeline.get_info()}): {exc}")

                # propagate
                raise
