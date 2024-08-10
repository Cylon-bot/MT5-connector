import logging
import sys
from typing import Dict, Any

YAML_TYPE = Dict[Any, Any]

TIMEFRAME_M1: int = 1
TIMEFRAME_M2: int = 2
TIMEFRAME_M3: int = 3
TIMEFRAME_M4: int = 4
TIMEFRAME_M5: int = 5
TIMEFRAME_M6: int = 6
TIMEFRAME_M10: int = 10
TIMEFRAME_M12: int = 12
TIMEFRAME_M15: int = 15
TIMEFRAME_M20: int = 20
TIMEFRAME_M30: int = 30
TIMEFRAME_H1: int = 1 | 0x4000
TIMEFRAME_H2: int = 2 | 0x4000
TIMEFRAME_H3: int = 3 | 0x4000
TIMEFRAME_H4: int = 4 | 0x4000
TIMEFRAME_H6: int = 6 | 0x4000
TIMEFRAME_H8: int = 8 | 0x4000
TIMEFRAME_H12: int = 12 | 0x4000
TIMEFRAME_D1: int = 24 | 0x4000
TIMEFRAME_W1: int = 1 | 0x8000
TIMEFRAME_MN1: int = 1 | 0xC000

ORDER_TYPE_BUY = 0
ORDER_TYPE_BUY_LIMIT = 2
ORDER_TYPE_BUY_STOP = 4

ORDER_TYPE_SELL = 1
ORDER_TYPE_SELL_LIMIT = 3
ORDER_TYPE_SELL_STOP = 5

PIPS = 0.0001
PIPS_UJ = 0.01
MICRO_PIPS = 0.00001
MICRO_PIPS_UJ = 0.001

LOG_LEVEL = logging.INFO
logging.basicConfig(level=LOG_LEVEL)

mt5_conector_logger = logging.getLogger("mt5_conector_logger")
handler_logger_global = logging.StreamHandler(sys.stdout)
mt5_conector_logger.addHandler(handler_logger_global)
