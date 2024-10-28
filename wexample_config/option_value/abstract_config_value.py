from abc import abstractmethod
from types import UnionType
from typing import Any, Type
from pydantic import BaseModel, validator

from wexample_helpers.const.types import StringKeysDict, AnyList


class AbstractConfigValue(BaseModel):
    raw: Any

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._validate_raw_type()

    def _validate_raw_type(self):
        value_type = self.get_value_type()

        if hasattr(value_type, '__args__'):
            expected_types = value_type.__args__
        else:
            expected_types = (value_type,)

        valid = False
        for expected_type in expected_types:
            if isinstance(expected_type, type):
                if isinstance(self.raw, expected_type) or (
                    isinstance(self.raw, type) and issubclass(self.raw, expected_type)):
                    valid = True
                    break
            else:
                if isinstance(self.raw, expected_type):
                    valid = True
                    break

        if not valid:
            from wexample_config.exception.option import InvalidOptionValueTypeException
            raise InvalidOptionValueTypeException(
                f'Invalid type for value "{type(self.raw)}": '
                f'expected {value_type}')

    @staticmethod
    @abstractmethod
    def get_value_type() -> Type | UnionType:
        pass

    def is_of_type(self, value_type: type) -> bool:
        return isinstance(self.raw, value_type)

    def get_str(self) -> str:
        assert self.is_of_type(str)

        return self.raw

    def is_none(self) -> bool:
        return self.raw is None

    def is_str(self) -> bool:
        return self.is_of_type(str)

    def get_int(self) -> int:
        assert self.is_of_type(int)
        return self.raw

    def is_int(self) -> bool:
        return self.is_of_type(int)

    def get_dict(self) -> StringKeysDict:
        assert self.is_of_type(dict)
        return self.raw

    def is_dict(self) -> bool:
        return self.is_of_type(dict)

    def get_list(self) -> AnyList:
        assert self.is_of_type(list)
        return self.raw

    def is_list(self) -> bool:
        return self.is_of_type(list)

    def get_float(self) -> float:
        assert self.is_of_type(float)
        return self.raw

    def is_float(self) -> bool:
        return self.is_of_type(float)

    def get_bool(self) -> bool:
        assert self.is_of_type(bool)
        return self.raw

    def is_bool(self) -> bool:
        return self.is_of_type(bool)
