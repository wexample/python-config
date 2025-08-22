from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Optional

from wexample_config.config_value.config_value import ConfigValue
from wexample_helpers.helpers.dict import DICT_PATH_SEPARATOR_DEFAULT


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
        # If this ConfigValue holds a list/tuple,
        # wrap each element consistently as ConfigValue/NestedConfigValue.
        elif self.is_list() or self.is_tuple():
            seq = self.raw
            wrapped = [self._wrap(v) for v in seq]
            # Preserve tuple/list type
            self.raw = tuple(wrapped) if self.is_tuple() else wrapped

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
        # Return a NestedConfigValue so traversal always hits a node
        # capable of get_config_item. Element wrapping is handled in __init__.
        if isinstance(val, Sequence) and not isinstance(val, (str, bytes, bytearray)):
            return cls(raw=val)

        # Case 3: primitive / other types → unchanged
        return ConfigValue(raw=val)

    def get_config_item(self, key: Any, default: Any = None) -> Optional["ConfigValue"]:
        # Dict access by string key
        if self.is_dict() and isinstance(key, str) and key in self.raw:
            return self.raw[key]

        # List/Tuple access by integer index (also accept str indices like "0")
        if self.is_list() or self.is_tuple():
            idx: int | None = None
            if isinstance(key, int):
                idx = key
            elif isinstance(key, str) and (
                key.isdigit() or (key.startswith("-") and key[1:].isdigit())
            ):
                try:
                    idx = int(key)
                except ValueError:
                    idx = None
            if idx is not None:
                seq = self.raw
                if -len(seq) <= idx < len(seq):
                    return seq[idx]
        return ConfigValue(raw=default)

    def search(
        self,
        path: str,
        separator: str = DICT_PATH_SEPARATOR_DEFAULT,
    ) -> Optional["ConfigValue"]:
        """
        Traverse nested dict/list/tuple values by a separated path.
        Example: search("first.second.0.third").
        Returns a ConfigValue/NestedConfigValue if found, else None.
        Assumes nested containers are wrapped as NestedConfigValue.
        """
        if not path:
            return self

        current: ConfigValue | None = self
        for part in path.split(separator):
            if not isinstance(current, NestedConfigValue):
                return None
            current = current.get_config_item(part)
            if current is None:
                return None

        return current
