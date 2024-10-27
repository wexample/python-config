from types import UnionType
from typing import Type

from wexample_config.option.abstract_option import AbstractOption


class ChildrenOption(AbstractOption):
    @staticmethod
    def get_value_type() -> Type | UnionType:
        return list
