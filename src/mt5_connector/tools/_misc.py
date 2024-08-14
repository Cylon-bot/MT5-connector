"""
file with misc tools use by the library
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Union

import yaml

from mt5_connector.tools.global_object import YAML_TYPE


class Singleton(type):
    """assure that the given parent class is instanciated only once

    Args:
        type : type of the given class
    """

    _instances = {}

    def __call__(cls, *args, **kwargs) -> type:
        """return the instanciation of the given object

        Returns:
            type: the type of the given object
        """

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def clear(cls):
        """delete the given class from the Singleton instanciation
        """
        del cls._instances[cls]


def read_yaml(path_yaml: Union[str, Path]) -> YAML_TYPE:
    """read a yaml file

    Args:
        path_yaml (Union[str, Path]): path of the yaml file

    Returns:
        YAML_TYPE: a dict representing the given yaml content
    """

    with open(path_yaml, "r") as file:
        config_file = yaml.load(file, Loader=yaml.FullLoader)
    return config_file
