from __future__ import annotations

from typing import Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption

_RAW_VALUE_ALLOWED_TYPE = Union[str, dict[str, Any]]


class DemoUnionConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return _RAW_VALUE_ALLOWED_TYPE
