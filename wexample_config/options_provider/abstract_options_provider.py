from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Type

from pydantic import BaseModel

if TYPE_CHECKING:
    from wexample_config.config_option.abstract_config_option import (
        AbstractConfigOption,
    )


class AbstractOptionsProvider(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def get_options(cls) -> list[type["AbstractConfigOption"]]:
        pass
