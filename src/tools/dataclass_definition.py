from dataclasses import dataclass
from datetime import datetime

from typing import Optional


@dataclass
class TradeObject():
    """A dataclass object representing a Trade
    """
    symbol: str
    order_type: int
    ticket: int
    price: float
    sl: float
    tp: float
    risk: float
    comment: Optional[str] = None


@dataclass
class Candle():
    """A Dataclass object representing a Candle
    """
    time: datetime
    open: float
    close: float
    low: float
    high: float


@dataclass
class Order():
    """A Dataclass object representing an Order
    """
    pass
