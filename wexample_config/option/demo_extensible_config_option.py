from types import UnionType
from typing import Type

from wexample_config.option.abstract_config_option import AbstractConfigOption


class DemoExtensibleConfigOption(AbstractConfigOption):
    allow_undefined_keys: bool = True

    @staticmethod
    def get_allowed_types() -> Type | UnionType:
        return list
