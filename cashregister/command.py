import argparse
from pathlib import Path
from typing import Tuple

from cashregister.exceptions.command import FileNotFoundError

parser = argparse.ArgumentParser()
parser.add_argument(
    "--input",
    type=str,
    required=True,
    help="input file with transactions (owed, paid), ex.: 2.12,3.00",
)
parser.add_argument(
    "--output",
    type=str,
    default="result.out",
    help="output file which will store the change descrimination, ex.: 3 quarters,1 dime,3 pennies",
)


def parse_cli() -> Tuple[str, str]:
    """Get input and output file from command-line, and verify if the files exist.

    Returns:
       Tuple[str, str]: input and output filename

    Raises:
        FileNotFoundError: input file does not exist

    """
    cli_args = parser.parse_args()
    input = Path(cli_args.input)
    output = Path(cli_args.output)

    if not input.exists():
        raise FileNotFoundError(f"Input file does not exist: {input}")

    # TODO: review
    # if output.exists():
    # raise ValueError(f"Output file already exist: {output}")

    return (input.name, output.name)
