"""
file where all dataclass model are defined
"""

from dataclasses import dataclass, field
from datetime import datetime
from random import randint
from typing import Any, Dict, Optional

from errors.trade_error import NoPriceGiven
from tools.global_object import Order, OrderTypeFilling, OrderTypeTime, PendingOrder, TradeRequestActions


@dataclass
class TradeObject:
    """A dataclass object representing a Trade.

    Attr:
        symbol (str): The name of the trading instrument, for which the order is placed.
        order_type (Order): Order type. The value can be one of the values of the Order enumeration.
        deviation (float): Maximum acceptable deviation from the requested price, specified in points. Defaults to 20 points.
        ticket (int): Order ticket. Required for modifying pending orders.
        deal (int): deal id. Required for requesting trade after it is closed.
        price (Optional, float): Price at which an order should be executed. The price is not set in case of market orders having the DirectOrder type.
        sl (Optional, float): A price a Stop Loss order is activated at when the price moves in an unfavorable direction.
        tp (Optional, float): A price a Take Profit order is activated at when the price moves in a favorable direction.
        volume (Optional, float): Requested volume of a deal in lots. A real volume when making a deal depends on an order execution type. not needed if you have set a sl and a risk for your trade.
        risk (Optional, float): Risk of your trade. not needed if you have given a volume to your trade.
        expiration (Optional, datetime): Pending order expiration time.
        comment (Optional, str): Comment attach to an order.
    """

    symbol: str
    order_type: Order
    ticket: int = field(init=False)
    deal: int = field(init=False)
    deviation: float = 20
    price: Optional[float] = None
    volume: Optional[float] = None
    sl: Optional[float] = None
    tp: Optional[float] = None
    risk: Optional[float] = None
    expiration: Optional[datetime] = None
    comment: Optional[str] = None

    def __post_init__(self):
        """post initialization to check if the trade seems to be OK.

        Raises:
            ValueError: Raise the first ValueError if the user forgot to provide either a volume or either a risk AND sl.
            ValueError: Raise the second ValueError if the user gave a volume AND a risk which makes no sense.
        """
        if (self.risk is None or self.sl is None) and self.volume is None:
            raise ValueError("You need to either specified a risk AND sl OR a volume.")
        if self.risk is not None and self.volume is not None:
            raise ValueError("You need to chose between give a volume or give a risk.")
        if isinstance(self.order_type, PendingOrder) and self.price is None:
            raise NoPriceGiven("You need to give a price on your trade object for a pending order.")
        if not isinstance(self.order_type, Order):
            raise ValueError("Unrecognized trade order type on your trade object.")


@dataclass
class Candle:
    """A Dataclass object representing a Candle.

    Attr:
        time (datetime): time of the Candle.
        open (float): open of the Candle.
        high (float): high of the Candle, in the case of this is the current candle this value can change over time.
        low (float): low of the Candle, in the case of this is the current candle this value can change over time.
        close (float): close of the Candle, in the case of this is the current candle this value can change over time.
    """

    time: datetime
    open: float
    high: float
    low: float
    close: float


@dataclass
class MarketOrder:
    """A Dataclass object representing an order on the market.

    Attr:
        action (TradeRequestActions): Trading operation type. The value can be one of the values of the TradeRequestActions enumeration.
        magic (int): EA ID. Allows arranging the analytical handling of trading orders. Each EA can set a unique ID when sending a trading request.
        ticket (Optional, int): Order ticket. Required for modifying pending orders.
        symbol (Optional, str): The name of the trading instrument, for which the order is placed. Not required when modifying orders and closing positions.
        volume (Optional, float): Requested volume of a deal in lots. A real volume when making a deal depends on an order execution type.
        price (Optional, float): Price at which an order should be executed. The price is not set in case of market orders having the DirectOrder type.
        sl (Optional, float): A price a Stop Loss order is activated at when the price moves in an unfavorable direction.
        tp (Optional, float): A price a Take Profit order is activated at when the price moves in a favorable direction.
        deviation (Optional, float): Maximum acceptable deviation from the requested price, specified in points.
        order_type (Optional, Order): Order type. The value can be one of the values of the Order enumeration.
        type_filling (Optional, OrderTypeFilling): Order filling type. The value can be one of the OrderTypeFilling values.
        type_time (Optional, OrderTypeTime): Order type by expiration. The value can be one of the OrderTypeTime values.
        position (Optional, int): Position ticket. Fill it when changing and closing a position for its clear identification. Usually, it is the same as the ticket of the order that opened the position.
        expiration (Optional, datetime): Pending order expiration time.
        comment (Optional, str): Comment attach to an order.
    """

    action: TradeRequestActions
    magic: int = field(init=False)
    ticket: Optional[int] = None
    symbol: Optional[str] = None
    volume: Optional[float] = None
    price: Optional[float] = None
    sl: Optional[float] = None
    tp: Optional[float] = None
    deviation: Optional[float] = None
    order_type: Optional[Order] = None
    position: Optional[int] = None
    type_filling: Optional[OrderTypeFilling] = None
    type_time: Optional[OrderTypeTime] = None
    expiration: Optional[datetime] = None
    comment: Optional[str] = None

    def __post_init__(self):
        self.magic = randint(0, 1_000_000)

    def __dict__(self) -> Dict[str, Any]:
        dict_request = {
            "action": self.action,
            "magic": self.magic,
            "order": self.ticket,
            "symbol": self.symbol,
            "volume": self.volume,
            "price": self.price,
            "position": self.position,
            "sl": self.sl,
            "tp": self.tp,
            "deviation": self.deviation,
            "type": self.order_type,
            "type_filling": self.type_filling,
            "type_time": self.type_time,
            "expiration": self.expiration,
            "comment": self.comment,
        }

        return {key: value for key, value in dict_request.items() if value is not None}
