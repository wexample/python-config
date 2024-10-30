from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, Union, cast

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_value.callback_render_config_value import (
    CallbackRenderConfigValue,
)
from wexample_config.options_provider.abstract_options_provider import (
    AbstractOptionsProvider,
)

if TYPE_CHECKING:
    from wexample_config.config_value.config_value import ConfigValue


class AbstractNestedConfigOption(AbstractConfigOption):
    allow_undefined_keys: bool = False
    options: dict[str, AbstractConfigOption] = {}
    options_providers: Optional[list[type["AbstractOptionsProvider"]]] = None
    parent: Optional["AbstractConfigOption"] = None

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return dict[str, Any]

    def set_value(self, raw_value: Any) -> None:
        super().set_value(raw_value)

        if raw_value is None:
            return

        options = self.get_available_options()
        valid_option_names = {option_class.get_name() for option_class in options}

        if not self.allow_undefined_keys:
            unknown_keys = set(raw_value.keys()) - valid_option_names
            if unknown_keys:
                from wexample_config.exception.option import InvalidOptionException

                raise InvalidOptionException(
                    f"Unknown configuration option \"{', '.join(sorted(unknown_keys))}\", "
                    f'in "{self.__class__.__name__}", '
                    f"allowed options are: {', '.join(valid_option_names)}"
                )

        # Loop over options classes to execute option_class.resolve_config(config)
        # This will modify config before using it, with extra configuration keys.
        for option_class in options:
            raw_value = option_class.resolve_config(raw_value)

        # Resolve callables and process children recursively
        for key, child_raw_value in list(raw_value.items()):
            if isinstance(child_raw_value, CallbackRenderConfigValue):
                raw_value[key] = child_raw_value.render()

        for option_class in options:
            option_name = option_class.get_name()
            if option_name in raw_value:
                self.options[option_name] = option_class(
                    value=raw_value[option_name], parent=self
                )

    def get_options_providers(self) -> list[type["AbstractOptionsProvider"]]:
        if self.parent:
            return self.parent.get_options_providers()

        if self.options_providers:
            return self.options_providers

        return []

    def get_available_options(self) -> list[type["AbstractConfigOption"]]:
        providers = self.get_options_providers()
        options = []

        for provider in providers:
            options.extend(cast("AbstractOptionsProvider", provider).get_options())

        return options

    def get_option(
        self, option_type: Union[type["AbstractConfigOption"], str]
    ) -> Optional["AbstractConfigOption"]:
        option_name = (
            option_type.get_name() if not isinstance(option_type, str) else option_type
        )

        if option_name in self.options:
            return self.options[option_name]

        return None

    def get_option_recursive(
        self, option_type: Union[type["AbstractConfigOption"], str]
    ) -> Optional["AbstractConfigOption"]:
        option = self.get_option(option_type)

        if option is not None:
            return option

        for option in self.options.values():
            if isinstance(option, AbstractNestedConfigOption):
                found_option = option.get_option_recursive(option_type)
                if found_option is not None:
                    return found_option

        return None

    def get_option_value(
        self, option_type: type["AbstractConfigOption"], default: Any = None
    ) -> "ConfigValue":
        from wexample_config.config_value.config_value import ConfigValue

        option = self.get_option(option_type)
        if option:
            return cast("ConfigValue", option.value)

        return ConfigValue(raw=default)
