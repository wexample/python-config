from types import UnionType
from typing import Type, Any

from wexample_config.config_option.abstract_nested_config_option import AbstractNestedConfigOption


class DemoNestedConfigOption(AbstractNestedConfigOption):
    nested: bool = True

    @staticmethod
    def get_raw_value_allowed_type() -> Type | UnionType:
        return Any
