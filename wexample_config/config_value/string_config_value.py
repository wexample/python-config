from types import UnionType
from typing import Type

from wexample_config.config_value.config_value import ConfigValue


class StringConfigValue(ConfigValue):
    @staticmethod
    def get_allowed_types() -> Type | UnionType:
        return str
