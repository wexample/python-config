from typing import Optional

from pydantic import BaseModel

from wexample_config.const.types import StateItemConfig


class ConfigManager(BaseModel):
    config: Optional[StateItemConfig] = None
