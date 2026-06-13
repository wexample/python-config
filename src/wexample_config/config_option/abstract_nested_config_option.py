from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union, cast

# Keyed by tuple of provider classes (types are hashable and stable).
# The registry only depends on which providers are active, never on instance state.
_REGISTRY_CACHE: dict[tuple, dict] = {}

# Cache which option classes have a custom resolve_config (not the base no-op).
# Populated lazily on first encounter of each class.
_HAS_CUSTOM_RESOLVE: dict[type, bool] = {}

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_config.config_option.abstract_config_option import AbstractConfigOption

if TYPE_CHECKING:
    from wexample_config.config_value.config_value import ConfigValue
    from wexample_config.const.types import DictConfig
    from wexample_config.options_provider.abstract_options_provider import (
        AbstractOptionsProvider,
    )


@base_class
class AbstractNestedConfigOption(AbstractConfigOption):
    allow_undefined_keys: bool = public_field(
        description="Whether undefined keys are allowed",
        default=False,
    )
    options: dict[str, AbstractConfigOption] = public_field(
        description="Mapping of option keys to config options",
        factory=dict,
    )
    options_providers: list[type[AbstractOptionsProvider]] | None = public_field(
        description="Providers that can add additional options",
        default=None,
    )

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return Union[dict[str, Any], set[type[AbstractConfigOption]]]

    def dump(self) -> Any:
        return {name: option.dump() for name, option in self.options.items()}

    def get_allowed_options(self) -> list[type[AbstractConfigOption]]:
        providers = self.get_options_providers()
        return [option for provider in providers for option in provider.get_options()]

    def get_allowed_options_registry(self) -> dict[str, type[AbstractConfigOption]]:
        cache_key = (type(self), tuple(self.get_options_providers()))
        cached = _REGISTRY_CACHE.get(cache_key)
        if cached is not None:
            return cached

        options_registry = {
            option.get_name(): option for option in self.get_allowed_options()
        }
        _REGISTRY_CACHE[cache_key] = options_registry
        return options_registry

    def get_option(
        self, option_type: type[AbstractConfigOption] | str
    ) -> AbstractConfigOption | None:
        option_name = (
            option_type.get_name() if not isinstance(option_type, str) else option_type
        )

        return self.options.get(option_name)

    def get_option_recursive(
        self, option_type: type[AbstractConfigOption] | str
    ) -> AbstractConfigOption | None:
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
        self, option_type: type[AbstractConfigOption], default: Any = None
    ) -> ConfigValue:
        from wexample_config.config_value.config_value import ConfigValue

        option = self.get_option(option_type)
        if option:
            return cast(ConfigValue, option.get_value())

        return ConfigValue(raw=default)

    def get_options_providers(self) -> list[type[AbstractOptionsProvider]]:
        if self.parent:
            return self.parent.get_options_providers()

        if self.options_providers:
            return self.options_providers

        return []

    def iter_options_recursive(self) -> None:
        """Yield every option (including nested) under this holder."""
        for option in self.options.values():
            yield option
            if isinstance(option, AbstractNestedConfigOption):
                yield from option.iter_options_recursive()

    def set_value(self, raw_value: Any) -> None:
        # Config might have been modified
        raw_value = super().set_value(raw_value)

        if raw_value is None:
            return

        self._create_options(config=raw_value)

    def _create_options(
        self, config: DictConfig | set[type[AbstractConfigOption]]
    ) -> list[AbstractConfigOption]:
        from wexample_config.config_option.config_option import ConfigOption
        from wexample_config.config_value.callback_render_config_value import (
            CallbackRenderConfigValue,
        )
        from wexample_config.const.types import DictConfig
        from wexample_config.exception.invalid_option_exception import (
            InvalidOptionException,
        )

        options = self.get_allowed_options_registry()
        valid_option_names = set(options.keys())
        new_options = []

        # Normalize: accept a set of option classes and convert to dict[name -> instance]
        if isinstance(config, set):
            normalized: dict[str, AbstractConfigOption] = {}
            for option_class in config:
                instance = option_class(parent=self)
                normalized[option_class.get_name()] = instance

            # Reuse the rest of the logic by working with a dict
            config = cast(DictConfig, normalized)

        # Loop over all options classes to execute option_class.resolve_config(config)
        # This will modify config before using it, with extra configuration keys.
        # For instance, an option defining the content of a file may add the should_exist option to ensure existence.
        # Skip classes that haven't overridden the base no-op (checked once per class, cached).
        for option_class in options.values():
            has_custom = _HAS_CUSTOM_RESOLVE.get(option_class)
            if has_custom is None:
                has_custom = (
                    option_class.resolve_config
                    is not AbstractConfigOption.resolve_config
                )
                _HAS_CUSTOM_RESOLVE[option_class] = has_custom
            if has_custom:
                config = option_class.resolve_config(config)

        # Accept both dict configs and normalized set-of-types
        unknown_keys = set(config.keys()) - valid_option_names
        if unknown_keys:
            if not self.allow_undefined_keys:
                raise InvalidOptionException(
                    message=f"Unknown configuration option \"{', '.join(sorted(unknown_keys))}\", "
                    f'in "{self.__class__.__name__}", '
                    f"allowed options are: {', '.join(sorted(valid_option_names))}"
                )
            else:
                for option_name in unknown_keys:
                    if not isinstance(config[option_name], AbstractConfigOption):
                        # Wrap unknown options
                        config[option_name] = ConfigOption(
                            key=option_name, parent=self, value=config[option_name]
                        )

        # Resolve callables and process children recursively
        for key, child_raw_value in list(config.items()):
            if isinstance(child_raw_value, CallbackRenderConfigValue):
                config[key] = child_raw_value.render(self)

        for option_name, option_config in config.items():
            if isinstance(option_config, AbstractConfigOption):
                new_option = option_config
                new_option.parent = self
            else:
                new_option = options[option_name](
                    parent=self,
                    value=option_config,
                )

            self.options[new_option.get_key()] = new_option
            new_options.append(new_option)

        return new_options
