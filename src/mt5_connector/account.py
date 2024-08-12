"""
file to help you connect to A metatrader 5 Account
"""

from datetime import datetime, timedelta
import logging
from pathlib import Path
from typing import Optional, Union

import MetaTrader5 as mt5

from tools.global_object import mt5_connector_logger
from tools.misc import Singleton, read_yaml


class Account(metaclass=Singleton):
    """Create a new connection with MT5 API using configuration files.

    Attr:
        id_account (str): id of your MT5 account.
        psw_account (str): password of your MT5 account.
        server_account (str): server of your MT5 account.
        account_currency (str): currency symbol of your MT5 account.
        account_info (AccountInfo): info of your account given by the MT5 API.
    """

    id_account: str
    psw_account: str
    server_account: str
    account_currency: str
    account_info: mt5.AccountInfo

    def __init__(self, connection_file_path: Union[str, Path]) -> None:
        """Use the given yaml file path to connect to the metatrade5 account.

        example of a valid input file :
        ##########
        currency: EUR
        server  : MetaQuotes-Demo
        login   : test
        password: test
        ##########

        Args:
            connection_file_path (Union[str, Path]): path of your connection file path.

        Raises:
            ConnectionError: raise this error if a connection error occurs in MT5 API.
        """
        data_credential_file = read_yaml(connection_file_path)
        self.id_account = data_credential_file["login"]
        self.psw_account = data_credential_file["password"]
        self.server_account = data_credential_file["server"]
        self.account_currency = data_credential_file["currency"]
        mt5.initialize()
        authorized = mt5.login(
            self.id_account,
            self.psw_account,
            self.server_account,
        )
        self.account_info = mt5.account_info()
        if authorized:
            logging.info(
                f"Connected: Connecting to MT5 Client with account :\n"
                f"ID account : {self.id_account}\n"
                f"Server : {self.server_account}"
            )
        else:
            raise ConnectionError(
                "Failed to connect at account #{}, error code: {}".format(
                    self.id_account,
                    mt5.last_error(),
                )
            )

    def get_updated_account_info(self):
        """get the updated info of the account from MT5 API."""
        self.account_info = mt5.account_info()

    @staticmethod
    def get_order_history_by_date(date_from: datetime, date_to: datetime) -> tuple[mt5.TradeDeal]:
        """get history of trades from the connected account using dates.

        Args:
            date_from (datetime): date from which we get the historical trade (take care, this will take the metatrader5 time zone).
            date_to (datetime): date to which we get the historical trade (take care, this will take the metatrader5 time zone).

        Returns:
            tuple[mt5.TradeDeal]: return a tuple of TradeDeal object provided by MT5 API.
        """
        res = mt5.history_deals_get(date_from=date_from, date_to=date_to)
        if res is not None and res != ():
            return res
        else:
            return ()

    @staticmethod
    def get_order_history_by_ticket(ticket: int) -> tuple[mt5.TradeDeal]:
        """get history of trades from the connected account using ticket order.

        Args:
            ticket (int): ticket order use to retrieve historical trades

        Returns:
            tuple[mt5.TradeDeal]: return a tuple of TradeDeal object provided by MT5 API.
        """
        res = mt5.history_deals_get(ticket=ticket)
        if res is not None and res != ():
            return res
        else:
            return ()

    @staticmethod
    def get_positions(symbol: Optional[str] = None) -> tuple[mt5.TradePosition]:
        """return all on going positions from a specified symbol or from all symbol if not any are provided.

        Args:
            symbol (str, optional): return only the positions of the given symbol, give all position otherwise. Defaults to None.

        Returns:
            tuple[mt5.TradePosition]: return a tuple of TradePosition object provided by MT5 API.
        """
        if symbol is None:
            res = mt5.positions_get()
        else:
            res = mt5.positions_get(symbol=symbol)

        if res is not None and res != ():
            return res
        else:
            return ()

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
            mt5_connector_logger.info(
                f"this symbol: {symbol} is not visible in the broker trading list, trying to switch it on"
            )
            if not mt5.symbol_select(symbol, True):
                mt5_connector_logger.warning(
                    f"this symbol: {symbol} is not visible and cannot be selected in the broker trading list"
                )
                return False
        return True
