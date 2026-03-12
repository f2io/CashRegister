import math


class Division:
    @classmethod
    def is_divided_by(cls, value: float, divisor: float = 3) -> bool:
        """Check if a float number is divided by the divisor

        Args:
            value (float): value
            divisor (float, optional): the divisor. Defaults to 3.

        Returns:
            bool: if it is divided or not

        Note:
            module operator (%) like this one `(3.33 % 3) == 0` was return False, so this helper was created check this division.
        """
        div_result = round(value / divisor, 2)
        proof_result = div_result * divisor
        return math.isclose(proof_result, value)
