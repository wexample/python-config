from types import UnionType
from typing import Type, Any

from wexample_config.src.demo_config_class import DemoConfigClass


class DemoNestedConfigOption(DemoConfigClass):
    nested: bool = True

    @staticmethod
    def get_value_allowed_type() -> Type | UnionType:
        return Any


