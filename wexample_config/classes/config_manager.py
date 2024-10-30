from types import UnionType
from typing import List, Type, cast, Optional, Dict, Any, TYPE_CHECKING
from wexample_config.option.abstract_config_option import AbstractConfigOption
from wexample_config.options_provider.abstract_options_provider import AbstractOptionsProvider
from wexample_filestate.config_value.callback_option_value import CallbackOptionValue

if TYPE_CHECKING:
    from wexample_filestate.config_value.item_config_value import ItemConfigValue


class ConfigManager(AbstractConfigOption):
    allow_undefined_keys: bool = False
    options: Dict[str, AbstractConfigOption] = {}
    parent: Optional["ConfigManager"] = None
    options_providers: Optional[List[Type["AbstractOptionsProvider"]]] = None

    @staticmethod
    def get_value_allowed_type() -> Type | UnionType:
        return Dict[str, Any]

    def set_value(self, raw_value: Any) -> None:
        if raw_value is None:
            return

        super().set_value(raw_value)

        options = self.get_all_available_options()
        valid_option_names = {option_class.get_name() for option_class in options}

        if not self.allow_undefined_keys:
            unknown_keys = set(raw_value.keys()) - valid_option_names
            if unknown_keys:
                from wexample_config.exception.option import InvalidOptionException

                raise InvalidOptionException(
                    f"Unknown configuration option \"{', '.join(sorted(unknown_keys))}\", "
                    f"in \"{self.__class__.__name__}\", "
                    f"allowed options are: {', '.join(valid_option_names)}"
                )

        # Loop over options classes to execute option_class.resolve_config(config)
        # This will modify config before using it, with extra configuration keys.
        for option_class in options:
            raw_value = option_class.resolve_config(raw_value)

        # Resolve callables and process children recursively
        for key, child_raw_value in list(raw_value.items()):
            from types import FunctionType

            if isinstance(child_raw_value, FunctionType):
                raw_value[key] = child_raw_value(self, raw_value)
            elif isinstance(raw_value, CallbackOptionValue):
                raw_value[key] = child_raw_value.get_callable()(self, raw_value)

        for option_class in options:
            option_name = option_class.get_name()
            if option_name in raw_value:
                self.options[option_name] = option_class(
                    value=raw_value[option_name]
                )

    def get_nested_class(self, key: str, raw_value: dict):
        return self.__class__

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

    def get_option(self, option_type: Type["AbstractConfigOption"]) -> Optional["AbstractConfigOption"]:
        option_name = option_type.get_name()

        if option_name in self.options:
            return self.options[option_name]

        return None

    def get_option_recursive(self, option_type: Type["AbstractConfigOption"]) -> Optional["AbstractConfigOption"]:
        option = self.get_option(option_type)

        if option is not None:
            return option

        for option in self.options.values():
            if isinstance(option, ConfigManager):
                found_option = option.get_option_recursive(option_type)
                if found_option is not None:
                    return found_option

    def get_option_value(self, option_type: Type["AbstractConfigOption"], default: Any = None) -> "ItemConfigValue":
        from wexample_filestate.config_value.item_config_value import ItemConfigValue

        option = self.get_option(option_type)
        if option:
            return cast("ItemConfigValue", option.value)

        return ItemConfigValue(raw=default)
