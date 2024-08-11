from datetime import datetime, timedelta
from typing import List, Dict, Optional, Union

import MetaTrader5 as Mt5

import pytz


def get_data(
        symbols: List[str],
        time_frame: int,
        utc_from: datetime,
        date_to: datetime,
        backtest: bool = False,
        backtest_data: Optional[pd.DataFrame] = None,
) -> "mt5_object":
    """
    ask to the mt5 server for the data and add any specified indicator from ta-lib libraries
    indicator implemented at the moment :

        - EMA
        - bollinger band
    """
    pair_data = dict()
    if not backtest:
        for pair in symbols:
            date_to = datetime(
                date_to.year,
                date_to.month,
                date_to.day,
                hour=date_to.hour,
                minute=date_to.minute,
            )
            rates = Mt5.copy_rates_range(pair, time_frame, utc_from, date_to)
            rates_frame = pd.DataFrame(rates)
            rates_frame["time"] = pd.to_datetime(rates_frame["time"], unit="s")
            rates_frame.drop(rates_frame.tail(1).index, inplace=True)
            pair_data[pair] = rates_frame
    else:
        pair_data = backtest_data[f"TF {time_frame}"]
    return pair_data


def get_time_frame_needed(tf: int = TIMEFRAME_M1, number_day_of_data: int = 4) -> Dict[int, datetime]:
    """
    return three day of candles in a specified TF
    """
    now = datetime.now().astimezone(pytz.timezone("Etc/GMT-5"))
    now = datetime(now.year, now.month, now.day, hour=now.hour, minute=now.minute)
    three_day = now - timedelta(days=number_day_of_data)
    tf_from_date = {tf: three_day}
    return tf_from_date


def return_datas(
        symbols: List[str],
        tf_list: List[int],
        datas_for_lot: bool,
        backtest_data: Optional[pd.DataFrame] = None,
        number_day_of_data: int = 4
) -> Union[Dict[int, Dict[str, pd.DataFrame]], Dict[str, pd.DataFrame]]:
    """
    return datas candles with specified information. If we need to return
    information for size lot it will only be the last candle.
    """
    if backtest_data is not None:
        backtest = True
    else:
        backtest = False
    data_candles_all_tf = dict()
    date_to = datetime.now().astimezone(pytz.timezone("Etc/GMT-5"))
    for TF in tf_list:
        tf_from_date = get_time_frame_needed(TF, number_day_of_data)
        for time_frame, from_date in tf_from_date.items():
            data_candles_all_tf[time_frame] = get_data(
                symbols,
                time_frame,
                from_date,
                date_to,
                backtest,
                backtest_data,
            )
    if datas_for_lot:
        last_row_lot_all_pair = dict()
        for tf, data_candles in data_candles_all_tf.items():
            for pair, pair_data in data_candles.items():
                last_row_lot = pair_data.tail(1)
                last_row_lot_all_pair[pair] = last_row_lot
        return last_row_lot_all_pair
    else:
        return data_candles_all_tf
