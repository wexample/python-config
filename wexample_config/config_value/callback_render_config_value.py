from typing import Callable, Any

from wexample_config.config_value.config_value import ConfigValue


class CallbackRenderConfigValue(ConfigValue):
    @staticmethod
    def get_allowed_types() -> type:
        return Callable[..., Any]

    def render(self) -> str:
        return self.raw()
