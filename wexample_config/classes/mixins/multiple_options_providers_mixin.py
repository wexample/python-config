from abc import abstractmethod
from typing import List, Type, cast, Optional, Dict
from pydantic import BaseModel
from wexample_config.const.types import DictConfig
from wexample_config.option.abstract_option import AbstractOption
from wexample_config.options_provider.abstract_options_provider import AbstractOptionsProvider
from wexample_config.src.config_manager import ConfigManager


class MultipleOptionsProvidersMixin(BaseModel):
    config_manager: Optional[ConfigManager] = None
    _options: Dict[str, AbstractOption] = {}

    def __init__(self, config: Optional[DictConfig] = None, **data):
        super().__init__(**data)

        config = self.build_config(config)

        if config:
            self.configure(config)

    def build_config(self, config: Optional[DictConfig] = None) -> DictConfig:
        return config or {}

    def configure(self, config: Optional[DictConfig]) -> None:
        from wexample_config.src.config_manager import ConfigManager

        options = self.get_all_options()
        valid_option_names = {option_class.get_name() for option_class in options}

        unknown_keys = set(config.keys()) - valid_option_names
        if unknown_keys:
            from wexample_config.exception.option import InvalidOptionException
            raise InvalidOptionException(f'Unknown configuration option name: {unknown_keys}')

        # Loop over options classes to execute option_class.resolve_config(config)
        # This will modify config before using it, with extra configuration keys.
        for option_class in options:
            config = option_class.resolve_config(config)

        for option_class in options:
            option_name = option_class.get_name()
            if option_name in config:
                self._options[option_name] = option_class(
                    value=config[option_name]
                )

        self.config_manager = ConfigManager(config=config)

    @abstractmethod
    def get_options_providers(self) -> List[Type["AbstractOptionsProvider"]]:
        pass

    def get_all_options(self) -> List[Type["AbstractOption"]]:
        providers = self.get_options_providers()
        options = []

        for provider in providers:
            options.extend(cast("AbstractOptionsProvider", provider).get_options())

        return options
