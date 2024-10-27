from abc import ABC
from typing import Any

from pydantic import BaseModel


class AbstractOption(BaseModel, ABC):
    value: Any
