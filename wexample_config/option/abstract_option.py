from abc import ABC
from types import UnionType
from typing import Any, Optional, Type
from pydantic import BaseModel
from wexample_config.const.types import DictConfig
from wexample_config.config_value.config_value import ConfigValue
from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import HasSnakeShortClassNameClassMixin


class AbstractOption(BaseModel, HasSnakeShortClassNameClassMixin, ABC):
    value: Optional[ConfigValue] = None

    def __init__(self, value: Any, **data) -> None:
        super().__init__(**data)

        self.value = (self.get_value_class_type())(raw=value) if not isinstance(value, ConfigValue) else value

    def get_value_class_type(self) -> Type:
        return ConfigValue

    @classmethod
    def get_class_name_suffix(cls) -> Optional[str]:
        return 'Option'

    @classmethod
    def get_name(cls) -> str:
        return cls.get_snake_short_class_name()

    @staticmethod
    def resolve_config(config: "DictConfig") -> "DictConfig":
        return config

    @staticmethod
    def get_value_allowed_type() -> Type | UnionType:
        return ConfigValue
