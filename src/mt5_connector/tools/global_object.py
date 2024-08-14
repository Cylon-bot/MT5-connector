"""
file where all global object are defined
"""

from enum import Enum
import logging
import sys
from typing import Dict, Any

import MetaTrader5 as mt5

YAML_TYPE = Dict[Any, Any]


class Order(Enum):
    pass


class PendingOrder(Order):
    ORDER_TYPE_BUY_LIMIT = mt5.ORDER_TYPE_BUY_LIMIT
    ORDER_TYPE_SELL_LIMIT = mt5.ORDER_TYPE_SELL_LIMIT
    ORDER_TYPE_BUY_STOP = mt5.ORDER_TYPE_BUY_STOP
    ORDER_TYPE_SELL_STOP = mt5.ORDER_TYPE_SELL_STOP


class DirectOrder(Order):
    ORDER_TYPE_BUY = mt5.ORDER_TYPE_BUY
    ORDER_TYPE_SELL = mt5.ORDER_TYPE_SELL


class TradeRequestActions(Enum):
    TRADE_ACTION_DEAL = mt5.TRADE_ACTION_DEAL
    TRADE_ACTION_PENDING = mt5.TRADE_ACTION_PENDING
    TRADE_ACTION_SLTP = mt5.TRADE_ACTION_SLTP
    TRADE_ACTION_MODIFY = mt5.TRADE_ACTION_MODIFY
    TRADE_ACTION_REMOVE = mt5.TRADE_ACTION_REMOVE
    TRADE_ACTION_CLOSE_BY = mt5.TRADE_ACTION_CLOSE_BY


class OrderTypeFilling(Enum):
    ORDER_FILLING_FOK = mt5.ORDER_FILLING_FOK
    ORDER_FILLING_IOC = mt5.ORDER_FILLING_IOC
    ORDER_FILLING_RETURN = mt5.ORDER_FILLING_RETURN


class OrderTypeTime(Enum):
    ORDER_TIME_GTC = mt5.ORDER_TIME_GTC
    ORDER_TIME_DAY = mt5.ORDER_TIME_DAY
    ORDER_TIME_SPECIFIED = mt5.ORDER_TIME_SPECIFIED
    ORDER_TIME_SPECIFIED_DAY = mt5.ORDER_TIME_SPECIFIED_DAY


PIPS = 0.0001
PIPS_UJ = 0.01
MICRO_PIPS = 0.00001
MICRO_PIPS_UJ = 0.001

LOG_LEVEL = logging.INFO
logging.basicConfig(level=LOG_LEVEL)

mt5_connector_logger = logging.getLogger("mt5_conector_logger")
handler_logger_global = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler_logger_global.setFormatter(formatter)
mt5_connector_logger.addHandler(handler_logger_global)
mt5_connector_logger.propagate = 0
