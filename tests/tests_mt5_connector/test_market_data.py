from datetime import datetime
from mt5_connector.market_data import get_data
from tools.dataclass_definition import Candle


def test_get_data_ok(mocker):
    mocker_mt5_copy_rates_range = mocker.patch('mt5_connector.market_data.mt5.copy_rates_range',
                                               return_value=((10000, 1, 1, 1, 1), (10000000, 2, 2, 2, 2)))

    data = get_data("EURUSD", 1, datetime.now(), datetime.now())

    mocker_mt5_copy_rates_range.assert_called_once()
    assert data == [Candle(datetime(1970, 1, 1, 3, 46, 40), 1, 1, 1, 1), Candle(datetime(1970, 4, 26, 19, 46, 40), 2, 2, 2, 2)]


def test_get_data_empty(mocker):
    mocker_mt5_copy_rates_range = mocker.patch('mt5_connector.market_data.mt5.copy_rates_range', return_value=None)

    data = get_data("EURUSD", 1, datetime.now(), datetime.now())

    mocker_mt5_copy_rates_range.assert_called_once()
    assert not data

    mocker_mt5_copy_rates_range = mocker.patch('mt5_connector.market_data.mt5.copy_rates_range', return_value=[])

    data = get_data("EURUSD", 1, datetime.now(), datetime.now())

    mocker_mt5_copy_rates_range.assert_called_once()
    assert not data
