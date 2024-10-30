from types import UnionType
from typing import Type, List, Dict, Any

from wexample_config.config_option.abstract_nested_config_option import AbstractNestedConfigOption


class ChildrenConfigOption(AbstractNestedConfigOption):
    @staticmethod
    def get_allowed_types() -> Type | UnionType:
        return List[Dict[str, Any]]
