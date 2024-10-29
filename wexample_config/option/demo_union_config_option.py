from typing import Type, Union, Dict, Any
from types import UnionType

from wexample_config.option.abstract_config_option import AbstractConfigOption


class DemoUnionConfigOption(AbstractConfigOption):
    @staticmethod
    def get_value_allowed_type() -> Type | UnionType:
        return Union[str, Dict[str, Any]]
