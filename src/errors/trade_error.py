"""
file with all errors regarding trades
"""


class NoTradableSymbol(Exception):
    """Raise this error if you attempt to create a position on a no tradable symbol."""

    pass


class NoPriceGiven(Exception):
    """Raise this error if a you attempt to create a position that needs a price, but you didn't give any"""

    pass
