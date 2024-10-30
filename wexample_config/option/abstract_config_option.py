from abc import ABC
from types import UnionType

from typing import Any, Optional, Type

from pydantic import BaseModel
from wexample_config.config_value.config_value import ConfigValue
from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import HasSnakeShortClassNameClassMixin


class AbstractConfigOption(BaseModel, HasSnakeShortClassNameClassMixin, ABC):
    value: Optional[ConfigValue] = None

    def __init__(self, value: Any = None, **data) -> None:
        super().__init__(**data)
        self.set_value(value)

    def set_value(self, raw_value: Any):
        if raw_value is None:
            return

        raw_value = self.prepare_value(raw_value)
        config_value_class = self.get_value_class_type()

        # Check if value is valid for the config option,
        # reuse same method to validate types.
        config_value_class.validate_value_type(
            raw_value=raw_value,
            allowed_type=self.get_value_allowed_type()
        )

        self.value = config_value_class(raw=raw_value) if not isinstance(raw_value, ConfigValue) else raw_value

    def prepare_value(self, raw_value: Any) -> Any:
        return raw_value

    def get_value_class_type(self) -> Type[ConfigValue]:
        return ConfigValue

    @staticmethod
    def get_value_allowed_type() -> Type | UnionType:
        return Any
