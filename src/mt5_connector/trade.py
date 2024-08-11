from typing import Optional

import MetaTrader5 as mt5

from tools.dataclass_definition import TradeObject
from mt5_connector.account import Account
from tools.global_object import DIRECT_ORDERS, PENDING_ORDERS, mt5_connector_logger


class TradeManagement:
    """class use to manage a specified trade on MT5

    attr:
        trade (TradeObject): _description_
        account (Account): _description_
    """
    trade: TradeObject
    account: Account

    def __init__(
        self,
        trade_object: TradeObject,
        account: Account
    ):
        self.trade = trade_object
        if self.tp is not None:
            self.open_request["tp"] = self.tp
        if self.sl is not None:
            self.open_request["sl"] = self.sl
        self.account = account

    def open_position(
        self,
        size: Optional[float] = None,
    ) -> "response_mt5":
        """
        use to open a market order on the given symbol
        this market order can be :
            - direct sell
            - direct buy
            - buy limit
            - sell limit
            - buy stop
            - sell stop
        """
        request_open = {}
        symbol_is_tradable = self.check_symbol(self.trade.symbol)
        if not symbol_is_tradable:
            raise ValueError("failed to open position cause this symbol cannot be found or trade.")

        if self.trade.order_type in PENDING_ORDERS and self.price is None:
            raise ValueError("You need to give a price for a pending order")

        elif self.trade.order_type in DIRECT_ORDERS:
            request_open["deviation"] = 20
            self.finding_actual_price()
        else:
            raise ValueError("Unrocognized trade order type.")

        if size is None:
            request_open["volume"] = self.find_position_size_forex()
        else:
            request_open["volume"] = size

        result_open_request = mt5.order_send(self.request_open)
        iterator = 0
        while (
            result_open_request.comment == "Requote"
            or (result_open_request.comment == "Invalid price")
            or (result_open_request.comment == "No prices")
            or (result_open_request.comment == "Invalid volume")
        ) and iterator < 50:
            self.finding_actual_price()

            if size is None:
                request_open["volume"] = self.find_position_size_forex()
            else:
                request_open["volume"] = size

            result_open_request = mt5.order_send(self.request_open)
            iterator += 1
        if self.result_open_request.retcode != mt5.TRADE_RETCODE_DONE:
            mt5_connector_logger.error(f"Failed to send order, retcode: {result_open_request.retcode}")
            return result_open_request

    def finding_actual_price(self):
        """
        in case of a direct order, we need to find the actual price
        """
        if self.trade.order_type == mt5.ORDER_TYPE_BUY:
            self.trade.price = mt5.symbol_info_tick(self.symbol).ask
        elif self.trade.order_type == mt5.ORDER_TYPE_SELL:
            self.trade.price = mt5.symbol_info_tick(self.symbol).bid

    def close_position(self) -> "result_close_request":
        """
        close a position either pending or in going
        """
        all_trade_on_going = self.account.get_positions()
        if all_trade_on_going.empty:
            all_ticket_on_going_trade = []
        else:
            all_ticket_on_going_trade = list(all_trade_on_going["ticket"].iloc[:])
        history_trade = self.account.get_order_history()

        if history_trade.empty:
            all_ticket_history_trade = []
        else:
            all_ticket_history_trade = list(history_trade["order"].iloc[:])
        order_type_close = None
        price_close = None

        if self.trade.ticket in all_ticket_history_trade:
            raise ValueError("This order is no longer on pending or on going so cannot proceed to close")

        elif self.trade.ticket in all_ticket_on_going_trade:

            if (
                self.order_type == mt5.ORDER_TYPE_BUY
                or self.order_type == mt5.ORDER_TYPE_BUY_STOP
                or self.order_type == mt5.ORDER_TYPE_BUY_LIMIT
            ):
                order_type_close = mt5.ORDER_TYPE_SELL
                price_close = mt5.symbol_info_tick(self.symbol).bid
            elif (
                self.order_type == mt5.ORDER_TYPE_SELL
                or self.order_type == mt5.ORDER_TYPE_SELL_STOP
                or self.order_type == mt5.ORDER_TYPE_SELL_LIMIT
            ):
                order_type_close = mt5.ORDER_TYPE_BUY
                price_close = mt5.symbol_info_tick(self.symbol).ask
            close_request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbol,
                "volume": self.size,
                "type": order_type_close,
                "position": self.ticket_order,
                "price": price_close,
                "magic": 234000,
                "comment": "Close trade",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_FOK,
            }
        else:
            close_request = {
                "action": mt5.TRADE_ACTION_REMOVE,
                "order": self.trade.ticket,
                "magic": 234000,
                "comment": "Close trade",
            }
        result_close_request = mt5.order_send(close_request)

        while (
            result_close_request.comment == "Requote"
            and self.request_open["action"] == mt5.TRADE_ACTION_DEAL
        ):
            if (
                self.order_type == mt5.ORDER_TYPE_BUY
                or self.order_type == mt5.ORDER_TYPE_BUY_STOP
                or self.order_type == mt5.ORDER_TYPE_BUY_LIMIT
            ):
                price_close = mt5.symbol_info_tick(self.symbol).bid
                close_request["price"] = price_close
            elif (
                self.order_type == mt5.ORDER_TYPE_SELL
                or self.order_type == mt5.ORDER_TYPE_SELL_STOP
                or self.order_type == mt5.ORDER_TYPE_SELL_LIMIT
            ):
                price_close = mt5.symbol_info_tick(self.symbol).ask
                close_request["price"] = price_close
            result_close_request = mt5.order_send(close_request)

        if result_close_request.retcode != mt5.TRADE_RETCODE_DONE:
            mt5_connector_logger.error(f"Failed to close order :( \n {result_close_request}")
        else:
            mt5_connector_logger.info("Order successfully closed!")

        return result_close_request

    def move_tp(self, new_tp: float) -> None:
        """_summary_

        Args:
            new_tp (float): _description_
        """
        stop_loss_trade = self.trade.sl
        take_profit_trade = self.trade.tp
        symbol = self.trade.symbol
        ticket = self.trade.ticket
        trade_comment = self.trade.comment
        if float(take_profit_trade) != new_tp:
            modify_request = {
                "action": mt5.TRADE_ACTION_SLTP,
                "symbol": symbol,
                "sl": stop_loss_trade,
                "position": int(ticket),
                "tp": new_tp,
                "comment": trade_comment,
            }
            result_modify_request = mt5.order_send(modify_request)
            if result_modify_request.retcode != mt5.TRADE_RETCODE_DONE:
                raise ValueError(f"Failed to modify order, retcode: {result_modify_request.retcode}")
            else:
                mt5_connector_logger.info(f"successfully moved TP from {self.trade.tp} to {new_tp}")
                self.trade.tp = new_tp

    def move_sl(self, new_sl: float):
        """_summary_

        Args:
            new_sl (float): _description_
        """
        stop_loss_trade = self.trade.sl
        take_profit_trade = self.trade.tp
        symbol = self.trade.symbol
        ticket = self.trade.ticket
        trade_comment = self.trade.comment
        if float(stop_loss_trade) != new_sl:
            modify_request = {
                "action": mt5.TRADE_ACTION_SLTP,
                "symbol": symbol,
                "sl": new_sl,
                "position": int(ticket),
                "tp": take_profit_trade,
                "comment": trade_comment,
            }
            result_modify_request = mt5.order_send(modify_request)
            if result_modify_request.retcode != mt5.TRADE_RETCODE_DONE:
                raise ValueError(f"Failed to modify order, retcode: {result_modify_request.retcode}")
            else:
                mt5_connector_logger.info(f"successfully moved SL from {self.trade.sl} to {new_sl}")
                self.trade.sl = new_sl

    def find_position_size_forex(self) -> float:
        """help you found the lot for a forex trade.

        Returns:
            float: lot for the specified risk, sl and symbol
        """
        percentage_converter = 0.01
        risk_percentage = self.trade.risk * percentage_converter
        currency_2 = self.trade.symbol[3:6]
        sl_size = abs(self.trade.sl - self.trade.price)
        self.account.get_updated_account_info()
        balance = self.account.account_info.balance
        if currency_2.lower() == "jpy":
            jpy_pip_converter = 100
            pip_value = (balance * risk_percentage) / (sl_size * jpy_pip_converter)
        else:
            pip_value = (balance * risk_percentage) / sl_size
        one_lot_price = 100_000
        account_currency_conversion = self.find_account_currency_conversion()
        calculate_lot = (pip_value / one_lot_price) * account_currency_conversion
        lot_size = round(calculate_lot, 2)
        return lot_size

    def find_account_currency_conversion(self):
        """find the price conversion between the traded symbol and your account currency

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        currency_2 = self.trade.symbol[3:6]
        other_character = self.trade.symbol[6:]
        account_currency = self.account.account_currency
        if account_currency == currency_2:
            account_currency_conversion = 1
        else:
            symbol_to_convert = account_currency + currency_2 + other_character
            symbol_is_real = self.account.check_symbol(symbol_to_convert)
            if symbol_is_real:
                account_currency_conversion = mt5.symbol_info_tick(symbol_to_convert).bid
            else:
                symbol_to_convert = currency_2 + account_currency + other_character
                symbol_is_real = self.account.check_symbol(symbol_to_convert)
                if symbol_is_real:
                    account_currency_conversion = 1 / mt5.symbol_info_tick(symbol_to_convert).bid
                else:
                    raise ValueError(f"unable to find a lot for {currency_2 + account_currency + other_character}")
        return account_currency_conversion
