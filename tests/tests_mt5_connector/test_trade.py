from unittest.mock import MagicMock

import MetaTrader5
import pytest

from errors.trade_error import NoTradableSymbol
from mt5_connector.trade import TradeManagement
from tools.dataclass_definition import TradeObject
from tools.global_object import DirectOrder, PendingOrder


def test_open_position_ok_direct_order(mocker):
    account_magic_mock = MagicMock()
    account_magic_mock.check_symbol.return_value = True
    order_response_mock = MagicMock()
    order_response_mock.retcode = MetaTrader5.TRADE_RETCODE_DONE
    order_response_mock.order = "order test"
    order_response_mock.deal = "deal test"
    info_tick_mock = MagicMock()
    info_tick_mock.ask = 1.0

    mocker_mt5_symbol_info_tick = mocker.patch('mt5_connector.trade.mt5.symbol_info_tick', return_value=info_tick_mock)
    mocker_mt5_order_send = mocker.patch('mt5_connector.trade.mt5.order_send', return_value=order_response_mock)

    new_trade = TradeObject("EURUSD", DirectOrder.ORDER_TYPE_BUY, sl=1.09250, tp=1.1, volume=0.05)
    trade_management = TradeManagement(new_trade, account_magic_mock)
    res = trade_management.open_position()

    mocker_mt5_symbol_info_tick.assert_called_once()
    mocker_mt5_order_send.assert_called_once()
    assert res == order_response_mock


def test_open_position_ok_pending_order(mocker):
    account_magic_mock = MagicMock()
    account_magic_mock.check_symbol.return_value = True
    order_response_mock = MagicMock()
    order_response_mock.retcode = MetaTrader5.TRADE_RETCODE_DONE
    order_response_mock.order = "order test"
    order_response_mock.deal = "deal test"
    info_tick_mock = MagicMock()
    info_tick_mock.ask = 1.0

    mocker_mt5_symbol_info_tick = mocker.patch('mt5_connector.trade.mt5.symbol_info_tick', return_value=info_tick_mock)
    mocker_mt5_order_send = mocker.patch('mt5_connector.trade.mt5.order_send', return_value=order_response_mock)

    new_trade = TradeObject("EURUSD", PendingOrder.ORDER_TYPE_BUY_LIMIT, sl=1.09250, tp=1.1, volume=0.05, price=1.0)
    trade_management = TradeManagement(new_trade, account_magic_mock)
    res = trade_management.open_position()

    assert mocker_mt5_symbol_info_tick.call_count == 0
    mocker_mt5_order_send.assert_called_once()
    assert res == order_response_mock


def test_open_position_ok_without_volume(mocker):
    account_magic_mock = MagicMock()
    account_magic_mock.check_symbol.return_value = True
    account_magic_mock.get_updated_account_info.return_value = None
    account_magic_mock.account_info.balance.return_value = 1000
    order_response_mock = MagicMock()
    order_response_mock.retcode = MetaTrader5.TRADE_RETCODE_DONE
    order_response_mock.order = "order test"
    order_response_mock.deal = "deal test"
    info_tick_mock = MagicMock()
    info_tick_mock.ask = 1.0
    info_tick_mock.bid = 1.0

    mocker_mt5_symbol_info_tick = mocker.patch('mt5_connector.trade.mt5.symbol_info_tick', return_value=info_tick_mock)
    mocker_mt5_order_send = mocker.patch('mt5_connector.trade.mt5.order_send', return_value=order_response_mock)

    new_trade = TradeObject("EURUSD", DirectOrder.ORDER_TYPE_BUY, sl=1.09250, tp=1.1, risk=0.01)
    trade_management = TradeManagement(new_trade, account_magic_mock)
    res = trade_management.open_position()

    assert mocker_mt5_symbol_info_tick.call_count == 2
    mocker_mt5_order_send.assert_called_once()
    assert res == order_response_mock


def test_open_position_not_ok_symbol_not_tradable(mocker):
    account_magic_mock = MagicMock()
    account_magic_mock.check_symbol.return_value = False

    new_trade = TradeObject("EURUSD", DirectOrder.ORDER_TYPE_BUY, sl=1.09250, tp=1.1, volume=0.05)
    trade_management = TradeManagement(new_trade, account_magic_mock)
    with pytest.raises(NoTradableSymbol):
        trade_management.open_position()
