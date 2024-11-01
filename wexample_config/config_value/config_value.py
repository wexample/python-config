from types import UnionType
from typing import Any, Callable, Type, List, Optional

from pydantic import BaseModel

from wexample_config.config_value.filter.abstract_config_value_filter import AbstractConfigValueFilter
from wexample_helpers.const.types import AnyList, StringKeysDict
from wexample_helpers.helpers.type_helper import type_validate_or_fail

from wexample_config.exception.option import InvalidOptionValueTypeException
from wexample_config.exception.config_value import ConfigValueTypeException


class ConfigValue(BaseModel):
    filters: Optional[list[AbstractConfigValueFilter]] = []
    raw: Any

    @staticmethod
    def apply_filters(content, filters: list[AbstractConfigValueFilter]):
        for value_filter in filters:
            content = value_filter.apply_filter(content=content)

        return content

    def get_str(self, type_check: bool = True) -> str:
        return self.apply_filters(
            content=self.get_str(),
            filters=self.filters)

    def __init__(self, **data) -> None:
        super().__init__(**data)

        try:
            self.validate_value_type(
                raw_value=self.raw, allowed_type=self.get_allowed_types()
            )
        except InvalidOptionValueTypeException as e:
            raise ConfigValueTypeException(
                f"Configuration value initialization exception: \n"
                f"{self.__class__.__name__}: {e}"
            )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(type={type(self.raw).__name__}, value={self.raw})>"

    def __str__(self) -> str:
        return f"{self.__repr__}"

    @classmethod
    def validate_value_type(
        cls, raw_value: Any, allowed_type: type | UnionType
    ) -> None:
        try:
            type_validate_or_fail(
                value=raw_value,
                allowed_type=allowed_type,
            )
        except TypeError as e:
            raise InvalidOptionValueTypeException(f"{cls.__name__}: {e}")

    @staticmethod
    def get_allowed_types() -> Any:
        return Any

    def is_of_type(self, value_type: Any, value: Any) -> bool:
        if value_type is Callable:
            return callable(value)
        if isinstance(value_type, type):
            return isinstance(value, value_type)
        return False

    def _assert_type(
        self, expected_type: Any, value: Any, type_check: bool = True
    ) -> None:
        if type_check and not self.is_of_type(expected_type, value):
            raise TypeError(f"Expected {expected_type} but got {type(value)}")

    def _execute_nested_method(self, method: Callable[[], Any]) -> Any:
        if isinstance(self.raw, ConfigValue):
            return getattr(self.raw, method.__name__)(type_check=False)
        return self.raw

    def _resolve_nested(self) -> "ConfigValue":
        if isinstance(self.raw, ConfigValue):
            return self.raw._resolve_nested()
        return self

    def _get_nested_raw(self) -> Any:
        return self._resolve_nested().raw

    def is_none(self) -> bool:
        return self.raw is None

    # Type checking methods
    def is_class(self) -> bool:
        import inspect
        return inspect.isclass(self.raw)

    # Type checking methods
    def is_callable(self) -> bool:
        return self.is_of_type(Callable[..., Any], self._get_nested_raw())

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
    def _get_value_from_callback(
        self, expected_type: Any, method: Callable[..., Any], type_check: bool = True
    ) -> Any:
        value = self._execute_nested_method(method)
        self._assert_type(expected_type, value, type_check)
        return value

    def get_callable(self, type_check: bool = True) -> Callable:
        return self._get_value_from_callback(
            Callable[..., Any], self.get_callable, type_check
        )

    def get_class(self, type_check: bool = True) -> Type[Any]:
        if type_check:
            assert self.is_class()
        return self._get_nested_raw()

    def get_str(self, type_check: bool = True) -> str:
        return self._get_value_from_callback(str, self.get_str, type_check)

    def get_int(self, type_check: bool = True) -> int:
        return self._get_value_from_callback(int, self.get_int, type_check)

    def get_float(self, type_check: bool = True) -> float:
        return self._get_value_from_callback(float, self.get_float, type_check)

    def get_bool(self, type_check: bool = True) -> bool:
        return self._get_value_from_callback(bool, self.get_bool, type_check)

    def get_complex(self, type_check: bool = True) -> complex:
        return self._get_value_from_callback(complex, self.get_complex, type_check)

    def get_bytes(self, type_check: bool = True) -> bytes:
        return self._get_value_from_callback(bytes, self.get_bytes, type_check)

    def get_dict(self, type_check: bool = True) -> StringKeysDict:
        return self._get_value_from_callback(dict, self.get_dict, type_check)

    def get_list(self, type_check: bool = True) -> AnyList:
        return self._get_value_from_callback(list, self.get_list, type_check)

    def get_set(self, type_check: bool = True) -> set:
        return self._get_value_from_callback(set, self.get_set, type_check)

    def get_tuple(self, type_check: bool = True) -> tuple:
        return self._get_value_from_callback(tuple, self.get_tuple, type_check)

    # Setters
    def set_class(self, value: Type[Any], type_check: bool = True) -> None:
        self._assert_type(Callable, value, type_check)
        self.raw = value

    def set_callable(self, value: Callable, type_check: bool = True) -> None:
        self._assert_type(Callable, value, type_check)
        self.raw = value

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
        return str(self._execute_nested_method(self.get_str))

    def to_int(self) -> int:
        return int(self._execute_nested_method(self.get_int))

    def to_float(self) -> float:
        return float(self._execute_nested_method(self.get_float))

    def to_bool(self) -> bool:
        return bool(self._execute_nested_method(self.get_bool))

    def to_complex(self) -> complex:
        return complex(self._execute_nested_method(self.get_complex))

    def to_bytes(self) -> bytes:
        return bytes(self._execute_nested_method(self.get_bytes))

    def to_dict(self) -> StringKeysDict:
        return dict(self._execute_nested_method(self.get_dict))

    def to_list(self) -> AnyList:
        return list(self._execute_nested_method(self.get_list))

    def to_set(self) -> set:
        return set(self._execute_nested_method(self.get_set))

    def to_tuple(self) -> tuple:
        return tuple(self._execute_nested_method(self.get_tuple))
