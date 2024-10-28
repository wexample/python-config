from abc import ABC, abstractmethod
from types import UnionType
from typing import Any, Optional, Type

from pydantic import BaseModel

from wexample_config.const.types import ConfigValue, DictConfig
from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import HasSnakeShortClassNameClassMixin
from wexample_helpers.const.types import StringKeysDict, AnyList


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
    def resolve_config(config: "DictConfig") -> "DictConfig":
        return config

    def get_value(self) -> ConfigValue:
        return self.value

    def set_value(self, value: Any) -> None:
        self.value = value

    def is_of_type(self, value_type: type) -> bool:
        return isinstance(self.value, value_type)

    def get_str(self) -> str:
        value = self.get_value()
        assert isinstance(value, str)

        return value

    def is_none(self) -> bool:
        return self.value is None

    def is_str(self) -> bool:
        return self.is_of_type(str)

    def get_int(self) -> int:
        value = self.get_value()
        assert isinstance(value, int)

        return value

    def is_int(self) -> bool:
        return self.is_of_type(int)

    def get_dict(self) -> StringKeysDict:
        value = self.get_value()
        assert isinstance(value, dict)

        return value

    def is_dict(self) -> bool:
        return self.is_of_type(dict)

    def get_list(self) -> AnyList:
        value = self.get_value()
        assert isinstance(value, list)

        return value

    def is_list(self) -> bool:
        return self.is_of_type(list)

    def get_float(self) -> float:
        value = self.get_value()
        assert isinstance(value, float)

        return value

    def is_float(self) -> bool:
        return self.is_of_type(float)

    def get_bool(self) -> bool:
        value = self.get_value()
        assert isinstance(value, bool)

        return value

    def is_bool(self) -> bool:
        return self.is_of_type(bool)
