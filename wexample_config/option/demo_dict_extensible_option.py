from typing import Type, Dict, Any
from types import UnionType

from wexample_config.option.abstract_config_option import AbstractConfigOption


class DemoDictConfigOption(AbstractConfigOption):
    @staticmethod
    def get_value_allowed_type() -> Type | UnionType:
        return Dict[str, Dict[str, Any]]
