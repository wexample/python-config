from types import UnionType
from typing import Type, List, Dict, Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_option.abstract_nested_config_option import AbstractNestedConfigOption


class ChildrenConfigOption(AbstractNestedConfigOption):
    children: List["AbstractConfigOption"] = []

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return List[dict[str, Any]]

    @staticmethod
    def get_allowed_types() -> Type | UnionType:
        return List[dict[str, Any]]

    def set_value(self, raw_value: Any) -> None:
        # Skip direct parent which creates only one item.
        AbstractConfigOption.set_value(self, raw_value)

        if raw_value is None:
            return

        for child_config in raw_value:
            self.children.append(
                AbstractNestedConfigOption(
                    value=child_config,
                    parent=self
                )
            )

    def dump(self) -> Any:
        output = []

        for child in self.children:
            print(child.get_name())

            output.append(child.dump())

        return output
