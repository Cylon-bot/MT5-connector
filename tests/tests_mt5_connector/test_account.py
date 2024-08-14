from datetime import datetime
from unittest.mock import MagicMock
import pytest
from mt5_connector.connector.account import Account
from mt5_connector.tools._misc import Singleton


def test_account_connection_ok(mocker):
    mocker_mt5_initialize = mocker.patch('mt5_connector.connector.account.mt5.initialize', return_value=None)
    mocker_mt5_login = mocker.patch('mt5_connector.connector.account.mt5.login', return_value=True)
    mocker_mt5_account_info = mocker.patch('mt5_connector.connector.account.mt5.account_info', return_value=None)
    mocker_mt5_last_error = mocker.patch('mt5_connector.connector.account.mt5.last_error', return_value=None)

    Account("tests/tests_conf/test_conf.yaml")

    mocker_mt5_initialize.assert_called_once()
    mocker_mt5_login.assert_called_once()
    mocker_mt5_account_info.assert_called_once()
    assert mocker_mt5_last_error.call_count == 0

    Singleton.clear(Account)


def test_account_connection_not_ok(mocker):
    mocker_mt5_initialize = mocker.patch('mt5_connector.connector.account.mt5.initialize', return_value=None)
    mocker_mt5_login = mocker.patch('mt5_connector.connector.account.mt5.login', return_value=False)
    mocker_mt5_account_info = mocker.patch('mt5_connector.connector.account.mt5.account_info', return_value=None)
    mocker_mt5_last_error = mocker.patch('mt5_connector.connector.account.mt5.last_error', return_value=None)

    with pytest.raises(ConnectionError):
        Account("tests/tests_conf/test_conf.yaml")

    mocker_mt5_initialize.assert_called_once()
    mocker_mt5_login.assert_called_once()
    mocker_mt5_account_info.assert_called_once()
    mocker_mt5_last_error.assert_called_once()


def test_get_order_history_by_date_ok(mocker):
    mocker_mt5_history_orders_get = mocker.patch('mt5_connector.connector.account.mt5.history_orders_get', return_value=("this is a test",))
    res = Account.get_order_history_by_date(date_from=datetime.now(), date_to=datetime.now())
    mocker_mt5_history_orders_get.assert_called_once()
    assert res == ("this is a test",)


def test_get_order_history_by_date_empty(mocker):
    mocker_mt5_history_orders_get = mocker.patch('mt5_connector.connector.account.mt5.history_orders_get', return_value=None)
    res = Account.get_order_history_by_date(date_from=datetime.now(), date_to=datetime.now())
    mocker_mt5_history_orders_get.assert_called_once()
    assert res == ()

    mocker_mt5_history_orders_get = mocker.patch('mt5_connector.connector.account.mt5.history_orders_get', return_value=())
    res = Account.get_order_history_by_date(date_from=datetime.now(), date_to=datetime.now())
    mocker_mt5_history_orders_get.assert_called_once()
    assert res == ()


def test_get_order_history_by_ticket_ok(mocker):
    mocker_mt5_history_orders_get = mocker.patch('mt5_connector.connector.account.mt5.history_orders_get', return_value=("this is a test",))
    res = Account.get_order_history_by_ticket(ticket=1)
    mocker_mt5_history_orders_get.assert_called_once()
    assert res == ("this is a test",)


def test_get_order_history_by_ticket_empty(mocker):
    mocker_mt5_history_orders_get = mocker.patch('mt5_connector.connector.account.mt5.history_orders_get', return_value=None)
    res = Account.get_order_history_by_ticket(ticket=1)
    mocker_mt5_history_orders_get.assert_called_once()
    assert res == ()

    mocker_mt5_history_orders_get = mocker.patch('mt5_connector.connector.account.mt5.history_orders_get', return_value=())
    res = Account.get_order_history_by_ticket(ticket=1)
    mocker_mt5_history_orders_get.assert_called_once()
    assert res == ()


def test_get_positions_ok(mocker):
    mocker_mt5_positions_get = mocker.patch('mt5_connector.connector.account.mt5.positions_get', return_value=("this is a test 1",))
    res = Account.get_positions()
    mocker_mt5_positions_get.assert_called_once()
    assert res == ("this is a test 1",)

    mocker_mt5_positions_get = mocker.patch('mt5_connector.connector.account.mt5.positions_get', return_value=("this is a test 2",))
    res = Account.get_positions(symbol="EURUSD")
    mocker_mt5_positions_get.assert_called_once()
    assert res == ("this is a test 2",)


def test_get_positions_empty(mocker):
    mocker_mt5_positions_get = mocker.patch('mt5_connector.connector.account.mt5.positions_get', return_value=None)
    res = Account.get_positions()
    mocker_mt5_positions_get.assert_called_once()
    assert res == ()

    mocker_mt5_positions_get = mocker.patch('mt5_connector.connector.account.mt5.positions_get', return_value=())
    res = Account.get_positions(symbol="EURUSD")
    mocker_mt5_positions_get.assert_called_once()
    assert res == ()


def test_check_symbol_visible_ok(mocker):
    res_symbol_info = MagicMock()
    res_symbol_info.visible = True
    mocker_mt5_check_symbol = mocker.patch('mt5_connector.connector.account.mt5.symbol_info', return_value=res_symbol_info)
    res = Account.check_symbol("EURUSD")
    mocker_mt5_check_symbol.assert_called_once()
    assert res == True


def test_check_symbol_not_visible_ok(mocker):
    res_symbol_info = MagicMock()
    res_symbol_info.visible = False
    mocker_mt5_check_symbol = mocker.patch('mt5_connector.connector.account.mt5.symbol_info', return_value=res_symbol_info)
    mocker_mt5_symbol_select = mocker.patch('mt5_connector.connector.account.mt5.symbol_select', return_value=True)
    res = Account.check_symbol("EURUSD")
    mocker_mt5_check_symbol.assert_called_once()
    mocker_mt5_symbol_select.assert_called_once()
    assert res == True


def test_check_symbol_not_ok(mocker):
    mocker_mt5_check_symbol = mocker.patch('mt5_connector.connector.account.mt5.symbol_info', return_value=None)
    res = Account.check_symbol("EURUSD")
    mocker_mt5_check_symbol.assert_called_once()
    assert res == False


def test_check_symbol_not_visible_not_ok(mocker):
    res_symbol_info = MagicMock()
    res_symbol_info.visible = False
    mocker_mt5_check_symbol = mocker.patch('mt5_connector.connector.account.mt5.symbol_info', return_value=res_symbol_info)
    mocker_mt5_symbol_select = mocker.patch('mt5_connector.connector.account.mt5.symbol_select', return_value=False)
    res = Account.check_symbol("EURUSD")
    mocker_mt5_check_symbol.assert_called_once()
    mocker_mt5_symbol_select.assert_called_once()
    assert res == False
