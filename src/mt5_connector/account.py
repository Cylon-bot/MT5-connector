
"""
file to help you connect to A metatrader 5 Account

"""

from datetime import datetime, timedelta
import logging
from pathlib import Path
from typing import Union

import MetaTrader5 as mt5

from tools.global_object import mt5_connector_logger
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
        currency: EUR
        server  : MetaQuotes-Demo
        login   : test
        password: test
        ##########

        Args:
            connection_file_path (Union[str, Path]): path of your connection file path

        Raises:
            ConnectionError: raise this error if a connection error occurs in MT5 API
        """
        data_credential_file = read_yaml(connection_file_path)
        self.id_account = data_credential_file["login"]
        self.psw_account = data_credential_file["password"]
        self.server_account = data_credential_file["server"]
        self.account_currency = connection_file_path["currency"]
        self.account_info = mt5.account_info()
        mt5.initialize()
        authorized = mt5.login(self.id_account, self.psw_account, self.server_account)
        if authorized:
            logging.info(f"Connected: Connecting to MT5 Client with account :\n"
                         f"ID account : {self.id_account}\n"
                         f"Server : {self.server_account}")
        else:
            raise ConnectionError("Failed to connect at account #{}, error code: {}".format(
                self.id_account, mt5.last_error())
            )

    def get_updated_account_info(self) -> "mt5_object":
        """get the info of the account

        Returns:
            mt5_object: info of the account
        """
        self.account_info = mt5.account_info()

    @staticmethod
    def get_order_history(date_from: datetime = datetime.now() - timedelta(hours=24), date_to: datetime = datetime.now() + timedelta(hours=5)) -> "mt5_object":
        """get history of trades from the connected account

        Args:
            date_from (datetime, optional): _description_. Defaults to datetime.now()-timedelta(hours=24).
            date_to (datetime, optional): _description_. Defaults to datetime.now()+timedelta(hours=5).

        Returns:
            _type_: _description_
        """
        res = mt5.history_deals_get(date_from, date_to)
        if res is not None and res != ():
            return res
        else:
            return None

    @staticmethod
    def get_positions(symbol=None) -> "mt5_object":
        """return all on going positions from a specified symbol or from all symbol

        Args:
            symbol (_type_, optional): return only the position of the given symbol, give all position otherwise. Defaults to None.

        Returns:
            pd.DataFrame: _description_
        """
        if symbol is None:
            res = mt5.positions_get()
        else:
            res = mt5.positions_get(symbol=symbol)

        if res is not None and res != ():
            return res
        else:
            return None

    @staticmethod
    def check_symbol(symbol: str) -> bool:
        """check if the given symbol exist in the broker trading list

        Args:
            symbol (str): symbol to check

        Returns:
            bool: true if the symbol exist, false otherwise
        """
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            mt5_connector_logger.warning(f"this symbol: {symbol} has not been found in the broker trading list")
            return False

        if not symbol_info.visible:
            mt5_connector_logger.info(f"this symbol: {symbol} is not visible in the broker trading list, trying to switch it on")
            if not mt5.symbol_select(symbol, True):
                mt5_connector_logger.warning(f"this symbol: {symbol} is not visible and cannot be selected in the broker trading list")
                return False
        return True
