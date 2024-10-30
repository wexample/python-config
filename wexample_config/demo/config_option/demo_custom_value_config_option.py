from typing import Type
from types import UnionType

from wexample_config.config_value.custom_type_config_value import CustomTypeConfigValue
from wexample_config.config_option.abstract_config_option import AbstractConfigOption


class DemoCustomValueConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Type | UnionType:
        return CustomTypeConfigValue
