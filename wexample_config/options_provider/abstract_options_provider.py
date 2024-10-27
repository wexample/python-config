from abc import ABC
from pydantic import BaseModel
from typing import List, TYPE_CHECKING, Type

if TYPE_CHECKING:
    from wexample_config.option.abstract_option import AbstractOption


class AbstractOptionsProvider(BaseModel, ABC):
    @classmethod
    def get_options(cls) -> List[Type["AbstractOption"]]:
        pass
