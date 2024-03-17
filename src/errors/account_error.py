
from typing import Any


class ConnectionError(Exception):
    def __init__(self, id_account: str, mt5_error: Any) -> None:
        self.id_account = id_account
        self.mt5_error = mt5_error
    def __call__(self):
        return "Failed to connect at account #{}, error code: {}".format(
                    self.id_account, self.mt5_error)