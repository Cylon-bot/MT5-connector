from dataclasses import dataclass
from datetime import datetime

from typing import Optional, Dict, Any


@dataclass
class TradeObject():
    """A BaseModel object representing a Trade

    Args:
        BaseModel: Parent class
    """
    symbol: str
    symbol_conversion: str
    order_type: int
    date_entry: datetime
    price: float
    rr: float
    be: Optional[float]
    initial_sl: float
    sl: float
    initial_tp: float
    tp: float
    risk: float
    sl_to_be: bool = False
    win: Optional[bool] = None
    comment: Optional[str] = None
    additional_info: str = ""
    changing_tp_management: Optional[Dict[str, Any]]
    changing_sl_management: Optional[Dict[str, Any]]
