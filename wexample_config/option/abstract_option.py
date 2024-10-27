from abc import ABC
from typing import Any

from pydantic import BaseModel

from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import HasSnakeShortClassNameClassMixin


class AbstractOption(BaseModel, HasSnakeShortClassNameClassMixin, ABC):
    value: Any

    def get_class_name_suffix(self) -> str:
        return 'Option'

    @classmethod
    def get_name(cls) -> str:
        return cls.get_snake_short_class_name()
