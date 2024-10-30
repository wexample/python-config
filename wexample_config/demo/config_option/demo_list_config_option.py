from typing import Type, List
from types import UnionType

from wexample_config.config_option.abstract_config_option import AbstractConfigOption


class DemoListConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Type | UnionType:
        return List