import sys
import logging

from cashregister.command import parse_cli
from cashregister.exceptions.command import CashRegisterCommandError
from cashregister.exceptions.exception import (
    CashRegisterExceptionGroup,
)
from cashregister.factory import creator

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    try:
        input, output = parse_cli()
        dyn_handler = creator.create_dollar_denominator_with_random_case()
        dyn_handler.run(input=input, output=output)
    except CashRegisterCommandError as exc:
        # Command-line invalid
        print(f"Invalid command-line parameter: {str(exc)}", file=sys.stderr)
    except CashRegisterExceptionGroup as gexc:
        # Print out error details
        print(
            f"Error pre-condition violated: {str(gexc)}",
            file=sys.stderr,
        )
    except Exception:
        # Propagate unexpected error
        raise


if __name__ == "__main__":
    main()
