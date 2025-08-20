from collections.abc import Mapping, Sequence
from typing import Any, Optional

from wexample_config.config_value.config_value import ConfigValue


class NestedConfigValue(ConfigValue):
    def __init__(self, **data) -> None:
        super().__init__(**data)

        # If this ConfigValue holds a dict,
        # replace all nested dict values with NestedConfigValue.
        if self.is_dict():
            value_dict = self.raw
            # Iterate over a copy of items so we can safely modify in place
            for key, val in list(value_dict.items()):
                self.raw[key] = self._wrap(val)

    @classmethod
    def _wrap(cls, val: Any) -> ConfigValue:
        """
        Recursively wrap:
        - any dict into NestedConfigValue(raw=dict)
        - lists/tuples into the same type with wrapped elements
        - everything else unchanged
        """
        # Case 1: dict / Mapping → wrap in NestedConfigValue
        if isinstance(val, Mapping):
            return cls(raw=dict(val))

        # Case 2: sequences (list/tuple), but not str/bytes
        if isinstance(val, Sequence) and not isinstance(val, (str, bytes, bytearray)):
            wrapped = [cls._wrap(v) for v in val]
            return tuple(wrapped) if isinstance(val, tuple) else wrapped

        # Case 3: primitive / other types → unchanged
        return ConfigValue(raw=val)

    def get_config_item(self, key: str) -> Optional["ConfigValue"]:
        if self.is_dict() and key in self.raw:
            return self.raw[key]
        return None
