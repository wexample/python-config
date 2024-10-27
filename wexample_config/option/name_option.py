from typing import Type
from types import UnionType

from wexample_config.option.abstract_option import AbstractOption


class NameOption(AbstractOption):
    @staticmethod
    def get_value_type() -> Type | UnionType:
        return str
