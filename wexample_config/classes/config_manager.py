from abc import abstractmethod
from typing import List, Type, cast, Optional, Dict, Any, Union, TYPE_CHECKING
from pydantic import BaseModel

from wexample_config.const.types import DictConfig
from wexample_config.option.abstract_config_option import AbstractConfigOption
from wexample_config.options_provider.abstract_options_provider import AbstractOptionsProvider
from wexample_filestate.config_value.callback_option_value import CallbackOptionValue

if TYPE_CHECKING:
    from wexample_filestate.config_value.item_config_value import ItemConfigValue


class ConfigManager(BaseModel):
    options: Dict[str, AbstractConfigOption] = {}

    def build_config(self, config: Optional[DictConfig] = None) -> DictConfig:
        return config or {}

    def configure(self, config: Optional[DictConfig]) -> None:
        config = self.build_config(config)
        options = self.get_all_options()
        valid_option_names = {option_class.get_name() for option_class in options}

        unknown_keys = set(config.keys()) - valid_option_names
        if unknown_keys:
            from wexample_config.exception.option import InvalidOptionException

            raise InvalidOptionException(
                f"Unknown configuration option name: {', '.join(sorted(unknown_keys))}, "
                f"allowed options are: {', '.join(valid_option_names)}"
            )

        # Loop over options classes to execute option_class.resolve_config(config)
        # This will modify config before using it, with extra configuration keys.
        for option_class in options:
            config = option_class.resolve_config(config)

        # Resolve callables and process children recursively
        for key, value in list(config.items()):
            from types import FunctionType

            if isinstance(value, FunctionType):
                config[key] = value(self, config)
            elif isinstance(value, CallbackOptionValue):
                config[key] = value.get_callable()(self, config)

        for option_class in options:
            option_name = option_class.get_name()
            if option_name in config:
                self.options[option_name] = option_class(
                    value=config[option_name]
                )

    @abstractmethod
    def get_options_providers(self) -> List[Type["AbstractOptionsProvider"]]:
        pass

    def get_all_options(self) -> List[Type["AbstractConfigOption"]]:
        providers = self.get_options_providers()
        options = []

        for provider in providers:
            options.extend(cast("AbstractOptionsProvider", provider).get_options())

        return options

    def get_option(self, option_type: Type["AbstractConfigOption"]) -> Optional["AbstractConfigOption"]:
        option_name = option_type.get_name()

        if option_name in self.options:
            return self.options[option_name]

        return None

    def get_option_value(self, option_type: Type["AbstractConfigOption"], default: Any = None) -> "ItemConfigValue":
        from wexample_filestate.config_value.item_config_value import ItemConfigValue

        option = self.get_option(option_type)
        if option:
            return cast("ItemConfigValue", option.value)

        return ItemConfigValue(raw=default)
