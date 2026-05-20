"""
Benchmarks for wexample_config critical path.

Run with:
    pytest benchmarks/test_benchmark.py --benchmark-only

Notes:
- NestedConfigValue.__attrs_post_init__ mutates self.raw in-place (wraps children).
  Construction benchmarks therefore use fresh dict copies on each call via
  module-level factory functions — never passing the same dict constant twice.
- Read-only operations (search, to_dict, is_empty, map…) use pre-built instances.
"""

from __future__ import annotations

from wexample_config.config_value.config_value import ConfigValue
from wexample_config.config_value.config_value_collection import ConfigValueCollection
from wexample_config.config_value.nested_config_value import NestedConfigValue

# ---------------------------------------------------------------------------
# Raw data constants  (never passed directly to NestedConfigValue as raw=)
# ---------------------------------------------------------------------------

_SHALLOW_RAW = {"name": "test", "version": "1.0.0", "active": True, "count": 42}

_DEEP_RAW = {
    "app": {
        "server": {
            "host": "localhost",
            "port": 8080,
            "ssl": {"enabled": True, "cert": "/path/to/cert"},
        },
        "database": {"url": "postgres://localhost/db", "pool_size": 10},
    },
    "logging": {"level": "INFO", "handlers": ["console", "file"]},
}

_LARGE_FLAT_RAW = {f"key_{i}": f"value_{i}" for i in range(50)}

_LARGE_NESTED_RAW = {
    f"section_{i}": {f"opt_{j}": f"val_{i}_{j}" for j in range(10)}
    for i in range(10)
}

# ---------------------------------------------------------------------------
# Pre-built instances for read-only benchmarks
# ---------------------------------------------------------------------------

_SHALLOW = NestedConfigValue(raw=dict(_SHALLOW_RAW))
_DEEP = NestedConfigValue(raw=dict(_DEEP_RAW))
_LARGE_NESTED = NestedConfigValue(raw=dict(_LARGE_NESTED_RAW))

_CV_NONE = ConfigValue(raw=None)
_CV_EMPTY_STR = ConfigValue(raw="")
_CV_EMPTY_LIST = ConfigValue(raw=[])
_CV_NON_EMPTY_STR = ConfigValue(raw="hello world")
_CV_INT = ConfigValue(raw=42)


def _make_chain(depth: int) -> ConfigValue:
    """ConfigValue(ConfigValue(... ConfigValue(raw='leaf') ...)) at given depth."""
    v: ConfigValue = ConfigValue(raw="leaf")
    for _ in range(depth):
        v = ConfigValue(raw=v)
    return v


_CHAIN_1 = _make_chain(1)
_CHAIN_5 = _make_chain(5)
_CHAIN_10 = _make_chain(10)

_COLLECTION_10 = ConfigValueCollection.from_raw_values(list(range(10)))
_COLLECTION_100 = ConfigValueCollection.from_raw_values(list(range(100)))
_COLLECTION_STR_100 = ConfigValueCollection.from_raw_values(
    [f"item_{i}" for i in range(100)]
)

# ---------------------------------------------------------------------------
# NestedConfigValue._wrap  — entry point for all wrapping; called at init
# ---------------------------------------------------------------------------


def test_wrap_primitive(benchmark):
    """Wrap a scalar — fast path, returns a bare ConfigValue."""
    benchmark(NestedConfigValue._wrap, "hello")


def test_wrap_shallow_dict(benchmark):
    """Wrap a 4-key flat dict — one level of NestedConfigValue construction."""
    # _wrap copies the dict internally, so _SHALLOW_RAW is never mutated.
    benchmark(NestedConfigValue._wrap, _SHALLOW_RAW)


def test_wrap_deep_dict(benchmark):
    """Wrap a 4-level nested dict — recursive wrapping of all children."""
    benchmark(NestedConfigValue._wrap, _DEEP_RAW)


def test_wrap_list(benchmark):
    """Wrap a mixed list — exercises the Sequence branch."""
    benchmark(NestedConfigValue._wrap, ["a", "b", {"key": "val"}, 42])


# ---------------------------------------------------------------------------
# NestedConfigValue construction  — init triggers post_init wrapping of children
# Factory functions ensure a fresh dict copy on every benchmark iteration.
# ---------------------------------------------------------------------------


def _init_shallow() -> NestedConfigValue:
    return NestedConfigValue(raw=dict(_SHALLOW_RAW))


def _init_large_flat() -> NestedConfigValue:
    return NestedConfigValue(raw=dict(_LARGE_FLAT_RAW))


def _init_large_nested() -> NestedConfigValue:
    return NestedConfigValue(raw=dict(_LARGE_NESTED_RAW))


def test_nested_init_shallow(benchmark):
    """Construct from a 4-key flat dict."""
    benchmark(_init_shallow)


def test_nested_init_large_flat(benchmark):
    """Construct from a 50-key flat dict — stresses the post_init iteration loop."""
    benchmark(_init_large_flat)


def test_nested_init_large_nested(benchmark):
    """Construct from a 10×10 nested dict — full recursive wrap of 110 nodes."""
    benchmark(_init_large_nested)


# ---------------------------------------------------------------------------
# NestedConfigValue.search  — dot-path traversal; called on every config read
# ---------------------------------------------------------------------------


def test_search_one_level(benchmark):
    """Traverse a 1-segment path."""
    benchmark(_SHALLOW.search, "name")


def test_search_three_levels(benchmark):
    """Traverse a 3-segment path."""
    benchmark(_DEEP.search, "app.server.host")


def test_search_five_levels(benchmark):
    """Traverse a 5-segment path."""
    benchmark(_DEEP.search, "app.server.ssl.enabled")


def test_search_missing_key(benchmark):
    """Path that does not exist — exercises the early-exit / default branch."""
    benchmark(_DEEP.search, "app.nonexistent.key")


# ---------------------------------------------------------------------------
# NestedConfigValue.to_dict  — recursive unwrap back to native Python dict
# ---------------------------------------------------------------------------


def test_to_dict_shallow(benchmark):
    """Unwrap a 4-key flat NestedConfigValue."""
    benchmark(_SHALLOW.to_dict)


def test_to_dict_deep(benchmark):
    """Unwrap a multi-level nested structure."""
    benchmark(_DEEP.to_dict)


def test_to_dict_large_nested(benchmark):
    """Unwrap a 10×10 structure — stresses recursive _unwrap."""
    benchmark(_LARGE_NESTED.to_dict)


# ---------------------------------------------------------------------------
# NestedConfigValue.update_nested  — deep merge of a source dict into existing
# Calling repeatedly replaces the same keys each time; cost is representative.
# ---------------------------------------------------------------------------

_UPDATE_SMALL = {"name": "updated", "count": 99}
_UPDATE_DEEP = {
    "app": {"server": {"port": 9090}, "database": {"pool_size": 20}},
    "logging": {"level": "DEBUG"},
}


def test_update_nested_small(benchmark):
    """Merge a 2-key flat dict into a shallow NestedConfigValue."""
    target = NestedConfigValue(raw=dict(_SHALLOW_RAW))
    benchmark(target.update_nested, _UPDATE_SMALL)


def test_update_nested_deep(benchmark):
    """Deep-merge a 3-level source dict — exercises recursive _update_nested_recursive."""
    target = NestedConfigValue(raw=dict(_DEEP_RAW))
    benchmark(target.update_nested, _UPDATE_DEEP)


# ---------------------------------------------------------------------------
# NestedConfigValue.set_by_path  — write a value at a nested path
# Repeated calls replace the same key — cost remains stable across iterations.
# ---------------------------------------------------------------------------


def test_set_by_path_shallow(benchmark):
    """Set a value at depth 1."""
    target = NestedConfigValue(raw=dict(_SHALLOW_RAW))
    benchmark(target.set_by_path, "name", "new_name")


def test_set_by_path_deep(benchmark):
    """Set a value at depth 3."""
    target = NestedConfigValue(raw=dict(_DEEP_RAW))
    benchmark(target.set_by_path, "app.server.port", 443)


# ---------------------------------------------------------------------------
# ConfigValue._resolve_nested  — unwrap a chain of nested ConfigValue wrappers
# ---------------------------------------------------------------------------


def test_resolve_nested_depth_1(benchmark):
    """Resolve a 1-deep wrapper chain."""
    benchmark(_CHAIN_1._resolve_nested)


def test_resolve_nested_depth_5(benchmark):
    """Resolve a 5-deep wrapper chain."""
    benchmark(_CHAIN_5._resolve_nested)


def test_resolve_nested_depth_10(benchmark):
    """Resolve a 10-deep wrapper chain — worst-case recursive unwrap."""
    benchmark(_CHAIN_10._resolve_nested)


# ---------------------------------------------------------------------------
# ConfigValue.is_empty  — multi-branch emptiness check; called on every access
# ---------------------------------------------------------------------------


def test_is_empty_none(benchmark):
    benchmark(_CV_NONE.is_empty)


def test_is_empty_empty_string(benchmark):
    benchmark(_CV_EMPTY_STR.is_empty)


def test_is_empty_non_empty_string(benchmark):
    """Non-empty string — must evaluate every branch before returning False."""
    benchmark(_CV_NON_EMPTY_STR.is_empty)


def test_is_empty_empty_list(benchmark):
    benchmark(_CV_EMPTY_LIST.is_empty)


# ---------------------------------------------------------------------------
# ConfigValueCollection.map  — bulk transformation over a list of ConfigValues
# ---------------------------------------------------------------------------


def test_collection_map_10_items(benchmark):
    """Map a getter over 10 items."""
    benchmark(_COLLECTION_10.map, lambda item: item.get_int(type_check=False))


def test_collection_map_100_items(benchmark):
    """Map a getter over 100 items — stresses iteration and call overhead."""
    benchmark(_COLLECTION_100.map, lambda item: item.get_int(type_check=False))


def test_collection_get_str_collection(benchmark):
    """Full get_str_collection() on 100 string ConfigValues."""
    benchmark(_COLLECTION_STR_100.get_str_collection)


# ---------------------------------------------------------------------------
# DemoConfigManager.set_value  — full config processing pipeline
# pedantic + setup ensures a fresh manager instance for every round so we
# measure first-call cost (option registry build + option tree creation).
# ---------------------------------------------------------------------------


def test_config_manager_set_value_flat(benchmark):
    """set_value with a flat config: registry build + option instantiation."""
    from wexample_config.demo.demo_config_manager import DemoConfigManager

    def setup():
        return (DemoConfigManager(),), {}

    benchmark.pedantic(
        lambda m: m.set_value({"name": "bench", "children": []}),
        setup=setup,
        rounds=300,
    )


def test_config_manager_set_value_nested(benchmark):
    """set_value with a nested config: recursive option tree creation."""
    from wexample_config.demo.demo_config_manager import DemoConfigManager

    def setup():
        return (DemoConfigManager(),), {}

    benchmark.pedantic(
        lambda m: m.set_value({"demo_nested": {"name": "inner"}}),
        setup=setup,
        rounds=300,
    )


def test_config_manager_get_option_recursive(benchmark):
    """get_option_recursive DFS across a populated option tree."""
    from wexample_config.demo.config_option.demo_nested_config_option import (
        DemoNestedConfigOption,
    )
    from wexample_config.demo.demo_config_manager import DemoConfigManager

    manager = DemoConfigManager()
    manager.set_value({"demo_nested": {"name": "inner"}})
    benchmark(manager.get_option_recursive, DemoNestedConfigOption)


def test_config_manager_get_allowed_options_registry(benchmark):
    """Build the name→class options registry from providers (called on each set_value)."""
    from wexample_config.demo.demo_config_manager import DemoConfigManager

    manager = DemoConfigManager()
    benchmark(manager.get_allowed_options_registry)
