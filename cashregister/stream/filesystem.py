from cashregister.denomination.change import Change
from cashregister.stream.pipeline import ITraceablePipelineFile
from cashregister.handler.transaction import Transaction
from cashregister.exceptions.parser import InvalidEntryTransactionError


class PipelineTransactionFile(ITraceablePipelineFile[Transaction, Change]):
    """Pipeline to decode transaction and encode change using filesystem."""

    NEWLINE = "\n"
    SEPARATOR = ","

    def __init__(
        self,
        input: str,
        output: str,
        input_sep=SEPARATOR,
        output_discard_if_error=True,
    ):
        # TextIOWrapper
        self.input = open(input, "r")
        self.input_sep = input_sep
        self.output = open(output, "w")
        self.output_first_line = True
        self.output_discard_if_error = output_discard_if_error

        self.current_line = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.input.close()

        # Clean up
        if exc_type is not None and self.output_discard_if_error:
            self.output.truncate(0)
        self.output.close()

    def read(self) -> Transaction | None:
        """Parse transaction

        Returns:
            Transaction: return a transaction from decoding string line

        Raises:
            InvalidEntryTransactionError: When the row does not have expected number of columns.
        """
        line = self.input.readline()
        if not line:
            return None

        self.current_line += 1

        # Remove newline and split
        tx_input = line.replace(PipelineTransactionFile.NEWLINE, "").split(self.input_sep)

        # Error handler
        if len(tx_input) != 2:
            raise InvalidEntryTransactionError(f"Expected 2 attributes per line, got:{tx_input}")

        return Transaction.from_string(tx_input[0], tx_input[1])

    def write(self, output: Change):
        """Export change denomination"""
        newline = PipelineTransactionFile.NEWLINE
        if self.output_first_line:
            newline = ""
            self.output_first_line = False

        self.output.write(f"{newline}{str(output)}")

    def get_info(self) -> str:
        """Return current line"""
        return f"processing line:{self.current_line}"
