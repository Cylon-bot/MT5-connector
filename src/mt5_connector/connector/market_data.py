"""
file to help you get the data candle from MT5
"""

from datetime import datetime

import MetaTrader5 as mt5

from mt5_connector.tools.dataclass_definition import Candle, Tick


def get_data(symbol: str, time_frame: int, date_from: datetime, date_to: datetime) -> list[Candle]:
    """return the data of the specified symbol on the given time slot and timeframe.

    WARNING: The last candle is the current printing candle,
    so the close of this one is the current price and NOT THE REAL CLOSE.
    On the same basis, the low and high are not the final low and high for this candle, but just the current low and high.

    Args:
        symbols (str): symbol of the data you want to get
        time_frame (int): timeframe of the data you want to get
        date_from (datetime): date_from of the data you want to get
        date_to (datetime): date_to of the data you want to get

    Returns:
        list[Candle]: return a list of Candle object representing the data
    """
    data = mt5.copy_rates_range(
        symbol,
        time_frame,
        date_from,
        date_to,
    )

    if data is None:
        return []

    data = [
        Candle(
            datetime.fromtimestamp(candle[0], tz=None),
            candle[1],
            candle[2],
            candle[3],
            candle[4],
        )
        for candle in data
    ]
    return data


def get_current_tick(symbol: str) -> Tick:
    """get the current tick for a given symbol

    Args:
        symbol (str): symbol of the market instrument

    Returns:
        Tick: current tick of the given symbol
    """
    tick = mt5.symbol_info_tick(symbol)
    return Tick(time=datetime.fromtimestamp(tick[0], tz=None),
                bid=tick[1],
                ask=tick[2],
                last=tick[3],
                volume=tick[4],
                time_msc=datetime.fromtimestamp(tick[5]/1000.0, tz=None),
                flags=tick[6],
                volume_real=tick[7])
