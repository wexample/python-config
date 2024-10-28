from abc import abstractmethod
from types import UnionType
from typing import Any, Type
from pydantic import BaseModel, validator
from wexample_helpers.const.types import StringKeysDict, AnyList
from wexample_config.exception.option import InvalidOptionValueTypeException


class AbstractConfigValue(BaseModel):
    raw: Any

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._validate_value_type(self.raw)

    def _validate_value_type(self, value: Any):
        expected_type = self.get_value_type()

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
    @abstractmethod
    def get_value_type() -> Type | UnionType:
        pass

    def is_of_type(self, value_type: Type) -> bool:
        return isinstance(self.raw, value_type)

    def _assert_type(self, expected_type: Type) -> None:
        if self.is_of_type(expected_type):
            raise TypeError(f'Expected {expected_type} but got {type(self.raw)}')

    def get_str(self) -> str:
        self._assert_type(int)
        return self.raw

    def is_none(self) -> bool:
        return self.raw is None

    def is_str(self) -> bool:
        return self.is_of_type(str)

    def get_int(self) -> int:
        self._assert_type(int)
        return self.raw

    def is_int(self) -> bool:
        return self.is_of_type(int)

    def get_dict(self) -> StringKeysDict:
        self._assert_type(dict)
        return self.raw

    def is_dict(self) -> bool:
        return self.is_of_type(dict)

    def get_list(self) -> AnyList:
        self._assert_type(list)
        return self.raw

    def is_list(self) -> bool:
        return self.is_of_type(list)

    def get_float(self) -> float:
        self._assert_type(float)
        return self.raw

    def is_float(self) -> bool:
        return self.is_of_type(float)

    def get_bool(self) -> bool:
        self._assert_type(bool)
        return self.raw

    def is_bool(self) -> bool:
        return self.is_of_type(bool)

    def get_complex(self) -> complex:
        self._assert_type(complex)
        return self.raw

    def is_complex(self) -> bool:
        return self.is_of_type(complex)

    def get_bytes(self) -> bytes:
        self._assert_type(bytes)
        return self.raw

    def is_bytes(self) -> bool:
        return self.is_of_type(bytes)

    def get_set(self) -> set:
        self._assert_type(set)
        return self.raw

    def is_set(self) -> bool:
        return self.is_of_type(set)

    def get_tuple(self) -> tuple:
        self._assert_type(tuple)
        return self.raw

    def is_tuple(self) -> bool:
        return self.is_of_type(tuple)
