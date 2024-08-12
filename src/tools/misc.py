from datetime import datetime
from pathlib import Path
from typing import Any, Union

import yaml

from tools.global_object import YAML_TYPE


class Singleton(type):
    """assure that the given parent class is instanciated only once

    Args:
        type : type of the given class
    """

    _instances = {}

    def __call__(self, *args, **kwargs) -> type:
        """return the instanciation of the given object

        Returns:
            _type_: the type of the given object
        """

        if self not in self._instances:
            self._instances[self] = super(Singleton, self).__call__(*args, **kwargs)
        return self._instances[self]


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
