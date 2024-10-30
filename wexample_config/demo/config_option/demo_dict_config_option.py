from typing import Type, Dict, Any
from types import UnionType

from wexample_config.config_option.abstract_config_option import AbstractConfigOption


class DemoDictConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return Dict[str, Dict[str, Any]]
