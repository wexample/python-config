from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import attrs
from wexample_helpers.classes.base_class import BaseClass

if TYPE_CHECKING:
    from wexample_config.config_option.abstract_config_option import (
        AbstractConfigOption,
    )


@attrs.define(kw_only=True)
class AbstractOptionsProvider(BaseClass, ABC):
    @classmethod
    @abstractmethod
    def get_options(cls) -> list[type[AbstractConfigOption]]:
        pass

    @classmethod
    def get_options_registry(cls) -> dict[str, type[AbstractConfigOption]]:
        return {option.get_name(): option for option in cls.get_options()}
