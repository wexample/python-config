from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, Union, cast

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.options_provider.abstract_options_provider import AbstractOptionsProvider

class AbstractNestedConfigOption(AbstractConfigOption):
    options: Dict[str, AbstractConfigOption] = {}
    parent: Optional["AbstractNestedConfigOption"] = None
    options_providers: Optional[List[Type["AbstractOptionsProvider"]]] = None

    def set_value(self, raw_value: Any) -> None:
        super().set_value(raw_value)

        options = self.get_all_available_options()

        if self.value is None:
            return

    def get_options_providers(self) -> List[Type["AbstractOptionsProvider"]]:
        if self.parent:
            return self.parent.get_options_providers()

        if self.options_providers:
            return self.options_providers

        return []

    def get_all_available_options(self) -> List[Type["AbstractConfigOption"]]:
        providers = self.get_options_providers()
        options = []

        for provider in providers:
            options.extend(cast("AbstractOptionsProvider", provider).get_options())

        return options
