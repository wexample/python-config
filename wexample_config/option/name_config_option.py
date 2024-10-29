from typing import Type
from types import UnionType

from wexample_config.option.abstract_config_option import AbstractConfigOption


class NameConfigOption(AbstractConfigOption):
    @staticmethod
    def get_value_allowed_type() -> Type | UnionType:
        return str
