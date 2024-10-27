from typing import Optional

from pydantic import BaseModel

from wexample_config.const.types import DictConfig


class ConfigManager(BaseModel):
    config: Optional[DictConfig] = None
