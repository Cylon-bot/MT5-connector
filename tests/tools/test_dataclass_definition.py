import pytest
from errors.trade_error import NoPriceGiven
from tools.dataclass_definition import TradeObject
from tools.global_object import DirectOrder, PendingOrder


def test_trade_object_raise_value_error_1():
    with pytest.raises(ValueError):
        TradeObject("EURUSD", DirectOrder.ORDER_TYPE_BUY, sl=1.09250, tp=1.1)
    with pytest.raises(ValueError):
        TradeObject("EURUSD", DirectOrder.ORDER_TYPE_BUY, tp=1.1, risk=1.1)
    with pytest.raises(ValueError):
        TradeObject("EURUSD", DirectOrder.ORDER_TYPE_BUY, tp=1.1)


def test_trade_object_raise_value_error_2():
    with pytest.raises(ValueError):
        TradeObject("EURUSD", DirectOrder.ORDER_TYPE_BUY, risk=1.09250, tp=1.1, sl=1.2, volume=0.02)


def test_trade_object_raise_value_error_3():
    with pytest.raises(ValueError):
        TradeObject("EURUSD", None, tp=1.1, sl=1.2, volume=0.02)


def test_trade_object_raise_no_price_given():
    with pytest.raises(NoPriceGiven):
        TradeObject("EURUSD",  PendingOrder.ORDER_TYPE_BUY_LIMIT, tp=1.1, sl=1.2, volume=0.02)
