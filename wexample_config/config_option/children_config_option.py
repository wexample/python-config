from types import UnionType
from typing import Type, List, Dict, Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_option.abstract_nested_config_option import AbstractNestedConfigOption


class ChildrenConfigOption(AbstractNestedConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return List[dict[str, Any]]

    @staticmethod
    def get_allowed_types() -> Type | UnionType:
        return List[dict[str, Any]]

    def set_value(self, raw_value: Any) -> None:
        AbstractConfigOption.set_value(self, raw_value)

        if raw_value is None:
            return

        for child_config in raw_value:
            self.create_child(child_config=child_config)
