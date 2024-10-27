from abc import ABC, abstractmethod
from types import UnionType
from typing import Any, Optional, Type

from pydantic import BaseModel

from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import HasSnakeShortClassNameClassMixin


class AbstractOption(BaseModel, HasSnakeShortClassNameClassMixin, ABC):
    value: Any

    def __init__(self, value: Any) -> None:
        value_type = self.get_value_type()

        if hasattr(value_type, '__args__'):
            expected_types = value_type.__args__
        else:
            expected_types = (value_type,)

        valid = False
        for expected_type in expected_types:
            if isinstance(expected_type, type):
                if isinstance(value, expected_type) or (isinstance(value, type) and issubclass(value, expected_type)):
                    valid = True
                    break
            else:
                if isinstance(value, expected_type):
                    valid = True
                    break

        if not valid:
            from wexample_config.exception.option import InvalidOptionTypeException
            raise InvalidOptionTypeException(
                f'Invalid type for option "{self.get_name()}": '
                f'{type(value)}, '
                f'expected {value_type}')

        super().__init__(
            value=value,
        )

    @classmethod
    def get_class_name_suffix(cls) -> Optional[str]:
        return 'Option'

    @classmethod
    def get_name(cls) -> str:
        return cls.get_snake_short_class_name()

    @staticmethod
    @abstractmethod
    def get_value_type() -> Type | UnionType:
        pass

    @staticmethod
    def resolve_config(config: "StateItemConfig") -> "StateItemConfig":
        return config
