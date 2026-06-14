from __future__ import annotations

from typing import Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption

_ALLOWED_TYPE = dict[str, dict[str, Any]]


class DemoDictConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return _ALLOWED_TYPE
