"""
file with all errors regarding account connection on MT5  
"""

from typing import Any


class ConnectionError(Exception):
    """Raise this error if a connection problem occurs when connecting to the MT5 API

    Args:
        Exception (_type_): Parent Exception class
    """

    def __init__(self, id_account: str, mt5_error: Any) -> None:
        """initialise this object

        Args:
            id_account (str): id of the account trying to connect to MT5 API
            mt5_error (Any): description of the error given by MT5
        """
        self.id_account = id_account
        self.mt5_error = mt5_error

    def __call__(self) -> str:
        """When call this Exception trigger this function

        Returns:
            str: return the error givent by MT5 in a good format
        """
        return "Failed to connect at account #{}, error code: {}".format(
            self.id_account,
            self.mt5_error,
        )
