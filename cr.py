import logging

from cashregister.command import parse_cli
from cashregister.factory import builder

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():

    input, output = parse_cli()
    dyn_handler = builder.build_dollar_denominator_with_random_case()
    dyn_handler.run(input=input, output=output)


if __name__ == "__main__":
    main()
