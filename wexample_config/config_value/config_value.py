from typing import Any, Type, Callable
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

    def _assert_type(self, expected_type: Type, value: Any, type_check: bool = True) -> None:
        if type_check and not self.is_of_type(expected_type, value):
            raise TypeError(f'Expected {expected_type} but got {type(value)}')

    def execute_nested_method(self, method: Callable[[], Any]) -> Any:
        if isinstance(self.raw, ConfigValue):
            return getattr(self.raw, method.__name__)(type_check=False)
        return self.raw

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

    def is_false(self) -> bool:
        return self.get_bool() == False

    def is_true(self) -> bool:
        return self.get_bool() == True

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
    def _get_value(self, expected_type: Type, method: Callable[[], Any], type_check: bool = True) -> Any:
        value = self.execute_nested_method(method)
        self._assert_type(expected_type, value, type_check)
        return value

    def get_str(self, type_check: bool = True) -> str:
        return self._get_value(str, self.get_str, type_check)

    def get_int(self, type_check: bool = True) -> int:
        return self._get_value(int, self.get_int, type_check)

    def get_float(self, type_check: bool = True) -> float:
        return self._get_value(float, self.get_float, type_check)

    def get_bool(self, type_check: bool = True) -> bool:
        return self._get_value(bool, self.get_bool, type_check)

    def get_complex(self, type_check: bool = True) -> complex:
        return self._get_value(complex, self.get_complex, type_check)

    def get_bytes(self, type_check: bool = True) -> bytes:
        return self._get_value(bytes, self.get_bytes, type_check)

    def get_dict(self, type_check: bool = True) -> StringKeysDict:
        return self._get_value(dict, self.get_dict, type_check)

    def get_list(self, type_check: bool = True) -> AnyList:
        return self._get_value(list, self.get_list, type_check)

    def get_set(self, type_check: bool = True) -> set:
        return self._get_value(set, self.get_set, type_check)

    def get_tuple(self, type_check: bool = True) -> tuple:
        return self._get_value(tuple, self.get_tuple, type_check)

    # Setters
    def set_str(self, value: str, type_check: bool = True) -> None:
        self._assert_type(str, value, type_check)
        self.raw = value

    def set_int(self, value: int, type_check: bool = True) -> None:
        self._assert_type(int, value, type_check)
        self.raw = value

    def set_float(self, value: float, type_check: bool = True) -> None:
        self._assert_type(float, value, type_check)
        self.raw = value

    def set_bool(self, value: bool, type_check: bool = True) -> None:
        self._assert_type(bool, value, type_check)
        self.raw = value

    def set_complex(self, value: complex, type_check: bool = True) -> None:
        self._assert_type(complex, value, type_check)
        self.raw = value

    def set_bytes(self, value: bytes, type_check: bool = True) -> None:
        self._assert_type(bytes, value, type_check)
        self.raw = value

    def set_dict(self, value: StringKeysDict, type_check: bool = True) -> None:
        self._assert_type(dict, value, type_check)
        self.raw = value

    def set_list(self, value: AnyList, type_check: bool = True) -> None:
        self._assert_type(list, value, type_check)
        self.raw = value

    def set_set(self, value: set, type_check: bool = True) -> None:
        self._assert_type(set, value, type_check)
        self.raw = value

    def set_tuple(self, value: tuple, type_check: bool = True) -> None:
        self._assert_type(tuple, value, type_check)
        self.raw = value

    # Conversion methods
    def to_str(self) -> str:
        return str(self.execute_nested_method(self.get_str))

    def to_int(self) -> int:
        return int(self.execute_nested_method(self.get_int))

    def to_float(self) -> float:
        return float(self.execute_nested_method(self.get_float))

    def to_bool(self) -> bool:
        return bool(self.execute_nested_method(self.get_bool))

    def to_complex(self) -> complex:
        return complex(self.execute_nested_method(self.get_complex))

    def to_bytes(self) -> bytes:
        return bytes(self.execute_nested_method(self.get_bytes))

    def to_dict(self) -> StringKeysDict:
        return dict(self.execute_nested_method(self.get_dict))

    def to_list(self) -> AnyList:
        return list(self.execute_nested_method(self.get_list))

    def to_set(self) -> set:
        return set(self.execute_nested_method(self.get_set))

    def to_tuple(self) -> tuple:
        return tuple(self.execute_nested_method(self.get_tuple))
