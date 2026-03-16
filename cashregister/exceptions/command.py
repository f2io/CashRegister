from cashregister.exceptions.exception import CashRegisterError


class CashRegisterCommandError(CashRegisterError):
    """Command-line error"""

    pass


class FileNotFoundError(CashRegisterCommandError):  # ValueError
    """Error file does not exist"""

    pass
