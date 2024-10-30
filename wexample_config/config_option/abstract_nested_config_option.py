from types import UnionType
from typing import Any, Dict, List, Optional, Type, Union, cast

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.options_provider.abstract_options_provider import AbstractOptionsProvider


class AbstractNestedConfigOption(AbstractConfigOption):
    options: Dict[str, AbstractConfigOption] = {}
    parent: Optional["AbstractNestedConfigOption"] = None
    options_providers: Optional[List[Type["AbstractOptionsProvider"]]] = None

    @staticmethod
    def get_raw_value_allowed_type() -> Type | UnionType:
        return Dict[str, Any]

    def set_value(self, raw_value: Any) -> None:
        super().set_value(raw_value)

        if self.value is None:
            return

        options = self.get_available_options()

        # Loop over options classes to execute option_class.resolve_config(config)
        # This will modify config before using it, with extra configuration keys.
        for option_class in options:
            raw_value = option_class.resolve_config(raw_value)

        for option_class in options:
            option_name = option_class.get_name()
            if option_name in raw_value:
                self.options[option_name] = option_class(
                    value=raw_value[option_name]
                )

    def get_options_providers(self) -> List[Type["AbstractOptionsProvider"]]:
        if self.parent:
            return self.parent.get_options_providers()

        if self.options_providers:
            return self.options_providers

        return []

    def get_available_options(self) -> List[Type["AbstractConfigOption"]]:
        providers = self.get_options_providers()
        options = []

        for provider in providers:
            options.extend(cast("AbstractOptionsProvider", provider).get_options())

        return options

    def get_option(
        self,
        option_type: Union[Type["AbstractConfigOption"], str]) -> Optional["AbstractConfigOption"]:
        option_name = option_type.get_name() if not isinstance(option_type, str) else option_type

        if option_name in self.options:
            return self.options[option_name]

        return None
