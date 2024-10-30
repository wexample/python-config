from typing import Type, Union
from types import UnionType

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_value.callback_render_config_value import CallbackRenderConfigValue


class NameConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Type | UnionType:
        return Union[str, CallbackRenderConfigValue]
