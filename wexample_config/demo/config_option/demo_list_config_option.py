from typing import Type, List, Any
from types import UnionType

from wexample_config.config_option.abstract_config_option import AbstractConfigOption


class DemoListConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return List
