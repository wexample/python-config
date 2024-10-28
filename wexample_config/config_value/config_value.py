from typing import Any, Type
from pydantic import BaseModel
from wexample_helpers.const.types import StringKeysDict, AnyList
from wexample_config.exception.option import InvalidOptionValueTypeException


class ConfigValue(BaseModel):
    raw: Any

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._validate_value_type(self.raw)

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

    def is_of_type(self, value_type: Type) -> bool:
        return isinstance(self.raw, value_type)

    def _assert_type(self, expected_type: Type) -> None:
        if self.is_of_type(expected_type):
            raise TypeError(f'Expected {expected_type} but got {type(self.raw)}')

    def is_none(self) -> bool:
        return self.raw is None

    # Type checking methods
    def is_str(self) -> bool:
        return self.is_of_type(str)

    def is_int(self) -> bool:
        return self.is_of_type(int)

    def is_float(self) -> bool:
        return self.is_of_type(float)

    def is_bool(self) -> bool:
        return self.is_of_type(bool)

    def is_complex(self) -> bool:
        return self.is_of_type(complex)

    def is_bytes(self) -> bool:
        return self.is_of_type(bytes)

    def is_dict(self) -> bool:
        return self.is_of_type(dict)

    def is_list(self) -> bool:
        return self.is_of_type(list)

    def is_set(self) -> bool:
        return self.is_of_type(set)

    def is_tuple(self) -> bool:
        return self.is_of_type(tuple)

    # Getter methods
    def get_str(self) -> str:
        self._assert_type(int)
        return self.raw

    def get_int(self) -> int:
        self._assert_type(int)
        return self.raw

    def get_float(self) -> float:
        self._assert_type(float)
        return self.raw

    def get_bool(self) -> bool:
        self._assert_type(bool)
        return self.raw

    def get_complex(self) -> complex:
        self._assert_type(complex)
        return self.raw

    def get_bytes(self) -> bytes:
        self._assert_type(bytes)
        return self.raw

    def get_dict(self) -> StringKeysDict:
        self._assert_type(dict)
        return self.raw

    def get_list(self) -> AnyList:
        self._assert_type(list)
        return self.raw

    def get_set(self) -> set:
        self._assert_type(set)
        return self.raw

    def get_tuple(self) -> tuple:
        self._assert_type(tuple)
        return self.raw

    # Conversion methods
    def to_str(self) -> str:
        return str(self.raw)

    def to_int(self) -> int:
        return int(self.raw)

    def to_float(self) -> float:
        return float(self.raw)

    def to_bool(self) -> bool:
        return bool(self.raw)

    def to_complex(self) -> complex:
        return complex(self.raw)

    def to_bytes(self) -> bytes:
        return bytes(self.raw)

    def to_dict(self) -> StringKeysDict:
        return dict(self.raw)

    def to_list(self) -> AnyList:
        return list(self.raw)

    def to_set(self) -> set:
        return set(self.raw)

    def to_tuple(self) -> tuple:
        return tuple(self.raw)
