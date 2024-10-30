from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List, TYPE_CHECKING, Type

if TYPE_CHECKING:
    from wexample_config.option.abstract_config_option import AbstractConfigOption


class AbstractOptionsProvider(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def get_options(cls) -> List[Type["AbstractConfigOption"]]:
        pass
