from cashregister.exceptions.exception import CashRegisterError


class InvalidFieldTypeTransactionError(CashRegisterError):  # ValueError
    """Error invalid owed and paid value type"""

    pass


class InvalidEntryTransactionError(CashRegisterError):  # ValueError
    """Error invalid rows"""

    pass


class InvalidDenominationError(CashRegisterError):
    """Error invalid denomination value"""

    pass
