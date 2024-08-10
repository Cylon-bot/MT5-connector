
"""
file to help you connect to A metatrader 5 Account

"""

import logging
from pathlib import Path
from typing import Union

import MetaTrader5 as Mt5

from tools.misc import Singleton, read_yaml


class Account(Singleton):
    """Create a new connection with MT5 API using configuration files

    Args:
        Singleton (Singleton object): assure that only one account is connected at the same time
    """

    def __init__(self, connection_file_path: Union[str, Path]):
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
        data_credential_file = read_yaml(connection_file_path)
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
