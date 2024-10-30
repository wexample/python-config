from typing import Any, Type, Union

from wexample_config.config_option.abstract_config_option import \
    AbstractConfigOption
from wexample_config.config_value.callback_render_config_value import \
    CallbackRenderConfigValue


class NameConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return Union[str, CallbackRenderConfigValue]
