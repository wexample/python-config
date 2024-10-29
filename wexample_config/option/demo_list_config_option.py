from typing import Type, List
from types import UnionType

from wexample_config.option.abstract_config_option import AbstractConfigOption


class DemoListConfigOption(AbstractConfigOption):
    @staticmethod
    def get_value_allowed_type() -> Type | UnionType:
        return List
