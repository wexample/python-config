from types import UnionType
from typing import Type

from wexample_config.option.abstract_config_option import AbstractConfigOption


class ChildrenConfigOption(AbstractConfigOption):
    @staticmethod
    def get_value_type() -> Type | UnionType:
        return list
