from typing import Any, Type
from pydantic import BaseModel
from wexample_helpers.const.types import StringKeysDict, AnyList
from wexample_config.exception.option import InvalidOptionValueTypeException


class ConfigValue(BaseModel):
    raw: Any

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._validate_value_type(self.raw)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(type={type(self.raw).__name__}, value={self.raw})>"

    def __str__(self) -> str:
        return f"{self.__repr__}"

    def _validate_value_type(self, value: Any):
        expected_type = self.get_value_type()

        if expected_type is Any:
            return value
        if hasattr(expected_type, '__args__'):
            expected_types = expected_type.__args__
        else:
            expected_types = (expected_type,)
        if not any(isinstance(value, t) for t in expected_types):
            raise InvalidOptionValueTypeException(
                f'Invalid type for value "{type(value)}": expected {expected_type}'
            )
        return value

    @staticmethod
    def get_value_type() -> Any:
        return Any

    def is_of_type(self, value_type: Type, value: Any) -> bool:
        return isinstance(value, value_type)

    def _assert_type(self, expected_type: Type, value: Any) -> None:
        if not self.is_of_type(expected_type, value):
            raise TypeError(f'Expected {expected_type} but got {type(value)}')

    def resolve_nested(self) -> "ConfigValue":
        if isinstance(self.raw, ConfigValue):
            return self.raw.resolve_nested()
        return self

    def _get_nested_raw(self) -> Any:
        return self.resolve_nested().raw

    def is_none(self) -> bool:
        return self.raw is None

    # Type checking methods
    def is_str(self) -> bool:
        return self.is_of_type(str, self._get_nested_raw())

    def is_int(self) -> bool:
        return self.is_of_type(int, self._get_nested_raw())

    def is_float(self) -> bool:
        return self.is_of_type(float, self._get_nested_raw())

    def is_bool(self) -> bool:
        return self.is_of_type(bool, self._get_nested_raw())

    def is_complex(self) -> bool:
        return self.is_of_type(complex, self._get_nested_raw())

    def is_bytes(self) -> bool:
        return self.is_of_type(bytes, self._get_nested_raw())

    def is_dict(self) -> bool:
        return self.is_of_type(dict, self._get_nested_raw())

    def is_list(self) -> bool:
        return self.is_of_type(list, self._get_nested_raw())

    def is_set(self) -> bool:
        return self.is_of_type(set, self._get_nested_raw())

    def is_tuple(self) -> bool:
        return self.is_of_type(tuple, self._get_nested_raw())

    # Getter methods
    def get_str(self) -> str:
        value = self._get_nested_raw()
        self._assert_type(str, value)
        return value

    def get_int(self) -> int:
        value = self._get_nested_raw()
        self._assert_type(int, value)
        return value

    def get_float(self) -> float:
        value = self._get_nested_raw()
        self._assert_type(float, value)
        return value

    def get_bool(self) -> bool:
        value = self._get_nested_raw()
        self._assert_type(bool, value)
        return value

    def get_complex(self) -> complex:
        value = self._get_nested_raw()
        self._assert_type(complex, value)
        return value

    def get_bytes(self) -> bytes:
        value = self._get_nested_raw()
        self._assert_type(bytes, value)
        return value

    def get_dict(self) -> StringKeysDict:
        value = self._get_nested_raw()
        self._assert_type(dict, value)
        return value

    def get_list(self) -> AnyList:
        value = self._get_nested_raw()
        self._assert_type(list, value)
        return value

    def get_set(self) -> set:
        value = self._get_nested_raw()
        self._assert_type(set, value)
        return value

    def get_tuple(self) -> tuple:
        value = self._get_nested_raw()
        self._assert_type(tuple, value)
        return value

    # Conversion methods
    def to_str(self) -> str:
        return str(self._get_nested_raw())

    def to_int(self) -> int:
        return int(self._get_nested_raw())

    def to_float(self) -> float:
        return float(self._get_nested_raw())

    def to_bool(self) -> bool:
        return bool(self._get_nested_raw())

    def to_complex(self) -> complex:
        return complex(self._get_nested_raw())

    def to_bytes(self) -> bytes:
        return bytes(self._get_nested_raw())

    def to_dict(self) -> StringKeysDict:
        return dict(self._get_nested_raw())

    def to_list(self) -> AnyList:
        return list(self._get_nested_raw())

    def to_set(self) -> set:
        return set(self._get_nested_raw())

    def to_tuple(self) -> tuple:
        return tuple(self._get_nested_raw())
