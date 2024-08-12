# MT5-connector
A library use to help you connect with metatrader5 API in python.

# Sumary
 In this library you can connect to your account in MT5, manage your trades and get data candles.

# Connect to your Account
to connect to your account use instanciate a Account object:

    from mt5_connector.account import Account

    account = Account("account_configuration.yaml")

your account configuration file needs to look like this:

    currency: EUR
    server  : MetaQuotes-Demo
    login   : test
    password: test

# create a new Trade

    from mt5_connector.trade import TradeManagement
    from mt5_connector.tools.dataclass_definition import TradeObject

    new_trade = TradeObject("EURUSD", DirectOrder.ORDER_TYPE_BUY, sl=1.09250, tp=1.1, volume=0.05)
    new_trade_management = TradeManagement(new_trade, account)

# close your trade

    new_trade_management.close_position()

or

    new_trade_management.close_position(volume_to_close)

where volume to close is a float corresponding to the amount of volume you want to close. (if you want to partially close your trade)

# modify your SL or TP

    new_trade_management.move_tp(your_new_tp)
    new_trade_management.move_sl(your_new_sl)