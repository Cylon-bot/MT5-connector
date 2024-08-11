import logging
import sys
from typing import Dict, Any

import MetaTrader5 as mt5

YAML_TYPE = Dict[Any, Any]

PENDING_ORDERS = [mt5.ORDER_TYPE_BUY_LIMIT, mt5.ORDER_TYPE_SELL_LIMIT,
                  mt5.ORDER_TYPE_BUY_STOP, mt5.ORDER_TYPE_SELL_STOP]
DIRECT_ORDERS = [mt5.ORDER_TYPE_BUY, mt5.ORDER_TYPE_SELL]

PIPS = 0.0001
PIPS_UJ = 0.01
MICRO_PIPS = 0.00001
MICRO_PIPS_UJ = 0.001

LOG_LEVEL = logging.INFO
logging.basicConfig(level=LOG_LEVEL)

mt5_connector_logger = logging.getLogger("mt5_conector_logger")
handler_logger_global = logging.StreamHandler(sys.stdout)
mt5_connector_logger.addHandler(handler_logger_global)
