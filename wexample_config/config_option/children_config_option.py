from types import UnionType
from typing import Type, List, Dict, Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption


class ChildrenConfigOption(AbstractConfigOption):
    @staticmethod
    def get_allowed_types() -> Type | UnionType:
        return List[Dict[str, Any]]
