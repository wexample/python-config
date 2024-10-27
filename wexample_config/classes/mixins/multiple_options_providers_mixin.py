from abc import abstractmethod, ABC
from typing import List, Type, cast, Optional

from wexample_config.const.types import DictConfig
from wexample_config.option.abstract_option import AbstractOption
from wexample_config.options_provider.abstract_options_provider import AbstractOptionsProvider
from wexample_config.src.config_manager import ConfigManager


class MultipleOptionsProvidersMixin(ABC):
    config_manager: Optional[ConfigManager] = None

    def __init__(self, config: Optional[DictConfig] = None, **data):
        super().__init__()

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

        self.config_manager = ConfigManager(config=config)

    @abstractmethod
    def get_options_providers(self) -> List[Type["AbstractOptionsProvider"]]:
        return []

    def get_all_options(self) -> List[Type["AbstractOption"]]:
        providers = self.get_options_providers()
        options = []

        for provider in providers:
            options.extend(cast("AbstractOptionsProvider", provider).get_options())

        return options
