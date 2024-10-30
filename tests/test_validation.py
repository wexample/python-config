from types import NoneType
from typing import Any, Dict, List, Union, Callable

import pytest
from wexample_config.config_value.config_value import ConfigValue
from wexample_config.exception.option import InvalidOptionValueTypeException
from wexample_helpers.helpers.type_helper import type_is_compatible


class TestConfigManager:
    def test_validation(self):
        def _test_callable() -> bool:
            return True

        success_cases = [
            ("str", Any),
            (True, Any),
            ("str", str),
            (123, int),
            (123.123, float),
            (None, NoneType),
            ([], list),
            ([], List),
            ({}, dict),
            ({}, Dict),
            ({"lorem": "ipsum"}, Dict[str, str]),
            ({"lorem": 123}, Dict[str, int]),
            ({}, Union[str, Dict[str, Any]]),
            (_test_callable, Callable),
            (_test_callable, Callable[..., Any]),
            (_test_callable, Callable[..., bool])
        ]

        failure_cases = [
            (123, str),
            ("123", int),
            (None, int),
            ({}, list),
            ([], dict),
            ({"lorem": 123}, Dict[str, str]),
            (123, Union[str, Dict[str, Any]]),
            (_test_callable, Callable[..., str])
        ]

        # Success cases: should not raise exceptions
        for value, expected_type in success_cases:
            ConfigValue.validate_value_type(value, expected_type)

        # Failure cases: should raise InvalidOptionValueTypeException
        for value, expected_type in failure_cases:
            with pytest.raises(InvalidOptionValueTypeException):
                ConfigValue.validate_value_type(value, expected_type)

    def test_compatibility(self):
        success_cases = [
            (str, Any),
            (bool, Any),
            (str, str),
            (int, int),
            (float, float),
            (type(None), type(None)),  # NoneType
            (list, list),
            (list, List),
            (dict, dict),
            (dict, Dict),
            (Dict[str, str], Dict[Any, Any]),
            (Dict[str, int], Dict[str, int]),
            (str, Union[str, Dict[str, Any]]),
            (Callable[..., bool], Callable),
            (Callable[..., bool], Callable),
            (Callable[..., Any], Callable[..., Any]),
            (Callable[..., bool], Callable[..., bool]),
            (Callable[..., bool], Callable[..., bool]),
            (Callable[..., Callable[..., str]], Callable[..., Callable]),
        ]

        failure_cases = [
            (int, str),
            (str, int),
            (type(None), int),  # NoneType incompatible with int
            (dict, list),
            (list, dict),
            (Dict[str, int], Dict[str, str]),
            (int, Union[str, Dict[str, Any]]),
            (Callable[..., bool], Callable[..., str])
        ]

        for actual_type, expected_type in success_cases:
            assert type_is_compatible(actual_type,
                                      expected_type), f"Expected {actual_type} to be compatible with {expected_type}"

        for actual_type, expected_type in failure_cases:
            assert not type_is_compatible(actual_type,
                                          expected_type), f"Expected {actual_type} to be incompatible with {expected_type}"
