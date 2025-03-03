"""
file to help you manage a trade on MT5
"""

from typing import Optional

import MetaTrader5 as mt5

from mt5_connector.errors.trade_error import NoTradableSymbol
from mt5_connector.tools.dataclass_definition import MarketOrder, TradeObject
from mt5_connector.connector.account import Account
from mt5_connector.tools.global_object import (
    DirectOrder,
    OrderTypeFilling,
    OrderTypeTime,
    PendingOrder,
    TradeRequestActions,
    mt5_connector_logger,
)


class TradeManagement:
    """class use to manage a specified trade on MT5

    attr:
        trade (TradeObject): An TradeObject representing a trade on the market.
        account (Account): An Account object containing all MT5 account info.
    """

    trade: TradeObject
    account: Account

    def __init__(self, trade_object: TradeObject, account: Account) -> None:
        """initialise this object

        Args:
            trade_object (TradeObject): _description_
            account (Account): _description_
        """
        self.trade = trade_object
        self.account = account

    def open_position(self) -> mt5.OrderSendResult:
        """open a new position using the Trade attribute

        Raises:
            NoTradableSymbol: Raise this error if you attempt to create a position on a no tradable symbol.

        Returns:
            mt5.OrderSendResult: result sent by MT5
        """

        symbol_is_tradable = self.account.check_symbol(self.trade.symbol)
        if not symbol_is_tradable:
            raise NoTradableSymbol("failed to open position cause this symbol cannot be found or trade.")

        order_type_is_direct_order = isinstance(self.trade.order_type, DirectOrder)
        if order_type_is_direct_order:
            self.finding_current_price()

        if self.trade.volume is None:
            self.trade.volume = self.find_position_size_forex()

        open_request = MarketOrder(
            action=(
                TradeRequestActions.TRADE_ACTION_DEAL.value
                if order_type_is_direct_order

                else TradeRequestActions.TRADE_ACTION_PENDING.value
            ),
            symbol=self.trade.symbol,
            volume=self.trade.volume,
            price=self.trade.price,
            sl=self.trade.sl,
            tp=self.trade.tp,
            deviation=self.trade.deviation,
            order_type=self.trade.order_type.value,
            type_filling=OrderTypeFilling.ORDER_FILLING_FOK.value,
            type_time=OrderTypeTime.ORDER_TIME_GTC.value,
            expiration=self.trade.expiration,
            comment=self.trade.comment,
        )
        result_open_request = mt5.order_send(open_request.__dict__())

        if result_open_request.retcode != mt5.TRADE_RETCODE_DONE:
            mt5_connector_logger.error("Failed to send order")
        else:
            self.trade.ticket = result_open_request.order
            self.trade.ticket_deal = result_open_request.deal
            mt5_connector_logger.info("Order successfully opened!")
        return result_open_request

    def close_position(self, volume_to_close: Optional[float] = None) -> mt5.OrderSendResult:
        """close a position either pending or in going.

        Args:
            volume_to_close (Optional[float]): if no volume is provided, the position will be completely closed, oterwise it will be partially close by the amount of given volume.

        Returns:
            mt5.OrderSendResult: result sent by MT5
        """
        all_trade_on_going = [trade.ticket for trade in self.account.get_positions()]
        order_type_close = None
        price_close = None

        if self.trade.ticket in all_trade_on_going:

            if (
                self.trade.order_type == DirectOrder.ORDER_TYPE_BUY
                or self.trade.order_type == PendingOrder.ORDER_TYPE_BUY_STOP
                or self.trade.order_type == PendingOrder.ORDER_TYPE_BUY_LIMIT
            ):
                order_type_close = DirectOrder.ORDER_TYPE_SELL.value
                price_close = mt5.symbol_info_tick(self.trade.symbol).bid
            elif (
                self.trade.order_type == DirectOrder.ORDER_TYPE_SELL
                or self.trade.order_type == PendingOrder.ORDER_TYPE_SELL_STOP
                or self.trade.order_type == PendingOrder.ORDER_TYPE_SELL_LIMIT
            ):
                order_type_close = DirectOrder.ORDER_TYPE_BUY.value
                price_close = mt5.symbol_info_tick(self.trade.symbol).ask
            position = self.account.get_positions_by_ticket(self.trade.ticket)[0]
            close_request = MarketOrder(
                action=TradeRequestActions.TRADE_ACTION_DEAL.value,
                symbol=self.trade.symbol,
                volume=volume_to_close if volume_to_close is not None else position.volume,
                order_type=order_type_close,
                position=self.trade.ticket,
                price=price_close,
                type_filling=OrderTypeFilling.ORDER_FILLING_FOK.value,
                type_time=OrderTypeTime.ORDER_TIME_GTC.value,
                comment=self.trade.comment,
            )
        else:
            close_request = MarketOrder(action=TradeRequestActions.TRADE_ACTION_REMOVE.value,
                                        ticket=self.trade.ticket,
                                        comment=self.trade.comment)
        result_close_request = mt5.order_send(close_request.__dict__())

        if result_close_request.retcode != mt5.TRADE_RETCODE_DONE:
            mt5_connector_logger.error("Failed to close order")
        else:
            self.trade.closed_tickets.append(result_close_request.order)
            self.trade.closed_deals.append(result_close_request.deal)
            mt5_connector_logger.info("Order successfully closed!")

        return result_close_request

    def finding_current_price(self):
        """in case of a direct order, we need to find the actual price
        """
        if self.trade.order_type == DirectOrder.ORDER_TYPE_BUY:
            self.trade.price = mt5.symbol_info_tick(self.trade.symbol).ask
        elif self.trade.order_type == DirectOrder.ORDER_TYPE_SELL:
            self.trade.price = mt5.symbol_info_tick(self.trade.symbol).bid

    def move_tp(self, new_tp: float) -> Optional[mt5.OrderSendResult]:
        """move your tp on your on going trade

        Args:
            new_tp (float): new tp to set

        Returns:
            mt5.OrderSendResult: result sent by MT5 if the tp was moved
        """
        take_profit_trade = self.trade.tp
        if take_profit_trade != new_tp:
            modify_request = MarketOrder(
                action=TradeRequestActions.TRADE_ACTION_SLTP.value,
                symbol=self.trade.symbol,
                sl=self.trade.sl,
                tp=new_tp,
                position=self.trade.ticket,
                comment=self.trade.comment,
            )
            result_modify_request = mt5.order_send(modify_request.__dict__())
            if result_modify_request.retcode != mt5.TRADE_RETCODE_DONE:
                mt5_connector_logger.error("Failed to modify TP")
            else:
                mt5_connector_logger.info(f"successfully moved TP from {self.trade.tp} to {new_tp}")
                self.trade.tp = new_tp
            return result_modify_request

    def move_sl(self, new_sl: float) -> Optional[mt5.OrderSendResult]:
        """move your sl on your on going trade

        Args:
            new_sl (float): new sl to set

        Returns:
            mt5.OrderSendResult: result sent by MT5 if the sl was moved
        """
        stop_loss_trade = self.trade.sl
        if stop_loss_trade != new_sl:
            modify_request = MarketOrder(
                action=TradeRequestActions.TRADE_ACTION_SLTP.value,
                symbol=self.trade.symbol,
                sl=new_sl,
                tp=self.trade.tp,
                position=self.trade.ticket,
                comment=self.trade.comment,
            )
            result_modify_request = mt5.order_send(modify_request.__dict__())
            if result_modify_request.retcode != mt5.TRADE_RETCODE_DONE:
                mt5_connector_logger.error("Failed to modify SL")
            else:
                mt5_connector_logger.info(f"successfully moved SL from {self.trade.sl} to {new_sl}")
                self.trade.sl = new_sl
            return result_modify_request

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
        print(f"balance --> {balance}")
        print(f"symbol --> {self.trade.symbol}")
        if currency_2.lower() == "jpy":
            print("jpy")
            jpy_pip_converter = 100
            pip_value = (balance * risk_percentage) / (sl_size / jpy_pip_converter)
        else:
            print("not jpy")
            pip_value = (balance * risk_percentage) / sl_size
        print(f"pip_value --> {pip_value}")
        one_lot_price = 100_000
        account_currency_conversion = self.find_account_currency_conversion()
        print(f"account_currency_conversion --> {account_currency_conversion}")
        calculate_lot = (pip_value / one_lot_price) * account_currency_conversion
        lot_size = round(calculate_lot, 2)
        print(f"lot --> {lot_size}")
        return lot_size

    def find_account_currency_conversion(self) -> float:
        """find the price conversion between the traded symbol and your account currency

        Raises:
            ValueError: Raise this error if we were unable to find the lot for your symbol

        Returns:
            float: price conversion
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
