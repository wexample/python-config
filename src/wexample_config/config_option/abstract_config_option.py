from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from pydantic import BaseModel
from wexample_helpers.classes.mixin.has_simple_repr_mixin import HasSimpleReprMixin
from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import (
    HasSnakeShortClassNameClassMixin,
)
from wexample_helpers.classes.mixin.import_packages_mixin import ImportPackagesMixin

if TYPE_CHECKING:
    from wexample_config.config_value.config_value import ConfigValue
    from wexample_config.const.types import DictConfig


class AbstractConfigOption(
    ImportPackagesMixin, HasSnakeShortClassNameClassMixin, HasSimpleReprMixin, BaseModel
):
    config_value: ConfigValue | None = None
    import_packages: ClassVar[tuple[str, ...]] = (
        "wexample_config.options_provider.abstract_options_provider",
        "wexample_config.config_value.config_value",
    )
    key: str | None = None
    parent: AbstractConfigOption | None = None

    def __init__(self, value: Any = None, **kwargs) -> None:
        self.__class__.load_imports()
        BaseModel.__init__(self, **kwargs)
        ImportPackagesMixin.__init__(self)
        HasSnakeShortClassNameClassMixin.__init__(self)
        HasSimpleReprMixin.__init__(self)

        self.key = self.key or self.get_name()
        self.set_value(value)

    @classmethod
    def get_class_name_suffix(cls) -> str | None:
        return "ConfigOption"

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return Any

    @staticmethod
    def resolve_config(config: DictConfig) -> DictConfig:
        return config

    def dump(self) -> Any:
        return self.get_value().raw

    def get_key(self) -> str:
        assert self.key is not None
        return self.key

    def get_parent(self) -> AbstractConfigOption:
        assert self.parent is not None
        return self.parent

    def get_root(self) -> AbstractConfigOption:
        if self.parent is not None:
            return self.parent.get_root()
        return self

    def get_value(self) -> ConfigValue | None:
        return self.config_value

    def get_value_class_type(self) -> type[ConfigValue]:
        from wexample_config.config_value.config_value import ConfigValue

        return ConfigValue

    def prepare_value(self, raw_value: Any) -> Any:
        return raw_value

    def set_value(self, raw_value: Any) -> Any:
        from wexample_config.config_value.config_value import ConfigValue

        if raw_value is None:
            return

        raw_value = self.prepare_value(raw_value)
        config_value_class = self.get_value_class_type()

        # Check if value is valid for the config option,
        # reuse same method to validate types.
        config_value_class.validate_value_type(
            raw_value=raw_value, allowed_type=self.get_raw_value_allowed_type()
        )

        self.config_value = (
            config_value_class(raw=raw_value)
            if not isinstance(raw_value, ConfigValue)
            else raw_value
        )

        return raw_value
