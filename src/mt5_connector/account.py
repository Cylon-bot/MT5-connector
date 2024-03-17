
"""
file to help you connect to A metatrader 5 Account

"""

import logging
from pathlib import Path
from typing import Union
import MetaTrader5 as Mt5
import yaml


class Account:
    """
    needed for connecting with the mt5 account
    """

    def __init__(
        self,
        account_currency: str = "USD",
        original_risk: float = 1,
    ):
        self.id_account = None
        self.psw_account = None
        self.server_account = None
        self.account_owner = None
        self.trade_open = False
        self.trade_on_going = {}
        self.trade_pending = {}
        self.account_currency = account_currency
        self.original_risk = original_risk

    def connect(self, connection_file_path: Union[str, Path]) -> None:
        """Use the given yaml file path to connect to the metatrade5 account.

        example of a valid input file :
        ##########
        Name     : Slim Shady
        Server   : MetaQuotes-Demo
        Login    : 4242424242
        Password : IamAVeryHardPasswordToCrack
        ##########
        you can use the file format given by mt5 when you create a demo account

        Args:
            connection_file_path (Union[str, Path]): path of your connection file path

        Raises:
            ConnectionError: raise this error if a connection error occurs in MT5 API
        """

        with open(connection_file_path) as credential_file:
            data_credential_file = yaml.load(credential_file, Loader=yaml.FullLoader)
        self.id_account = data_credential_file["Login"]
        self.psw_account = data_credential_file["Password"]
        self.server_account = data_credential_file["Server"]
        self.account_owner = data_credential_file["Name"]
        Mt5.initialize()
        authorized = Mt5.login(self.id_account, self.psw_account, self.server_account)
        if authorized:
            logging.info(f"Connected: Connecting to MT5 Client with account :\n"
                         f"Account owner : {self.account_owner}\n"
                         f"ID account : {self.id_account}\n"
                         f"Server : {self.server_account}")
        else:
            raise ConnectionError("Failed to connect at account #{}, error code: {}".format(
                self.id_account, Mt5.last_error())
            )

    def get_account_info(self) -> dict:
        """get the info of the account

        Returns:
            dict: info of the account
        """
        return Mt5.account_info()


class AccountSingleton:
    """
    assure that only one instance of Account is set at the same time
    """

    def __init__(self):
        """initialise instance
        """
        self.account = None

    def set(self, acc: Account):
        """set a New singletonAccount

        Args:
            acc (Account): the Account class instance

        Raises:
            RuntimeError: raise this if a singleton has already been set
        """
        if not self.account:
            self.account = acc
        else:
            raise RuntimeError("Singleton already set")

    def get(self) -> Account:
        """get the Account if one has been set

        Raises:
            RuntimeError: raise this if the account has not been set

        Returns:
            Account: instance of Account
        """
        if self.account:
            return self.account
        else:
            raise RuntimeError("Singleton unset")

    async def get_async(self) -> Account:
        """get the Account if one has been set (thread safe)

        Raises:
            RuntimeError: raise this if the account has not been set

        Returns:
            Account: instance of Account
        """
        if self.account:
            return self.account
        else:
            raise RuntimeError("Singleton unset")
