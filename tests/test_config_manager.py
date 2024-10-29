import pytest

from wexample_config.config_value.custom_type_config_value import CustomTypeConfigValue
from wexample_config.option.demo_custom_value_config_option import DemoCustomValueConfigOption
from wexample_config.option.demo_dict_config_option import DemoDictConfigOption
from wexample_config.option.demo_list_config_option import DemoListConfigOption
from wexample_config.option.demo_union_config_option import DemoUnionConfigOption
from wexample_config.src.demo_config_class import DemoConfigClass
from wexample_config.exception.option import InvalidOptionException, InvalidOptionValueTypeException


class TestConfigManager:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.test_object = DemoConfigClass()

    def test_setup(self):
        assert self.test_object is not None

    def test_configure_name(self):
        self.test_object.configure({
            "name": "yes"
        })

    def test_configure_unexpected(self):
        with pytest.raises(InvalidOptionException):
            self.test_object.configure({
                "unexpected_option": "yes"
            })

    def test_configure_unexpected_type(self):
        with pytest.raises(InvalidOptionValueTypeException):
            self.test_object.configure({
                "name": 123
            })

        with pytest.raises(InvalidOptionValueTypeException):
            self.test_object.configure({
                "name": []
            })

    def test_configure_list_type(self):
        with pytest.raises(InvalidOptionValueTypeException):
            self.test_object.configure({
                "demo_list": 123
            })

        self.test_object.configure({
            "demo_list": []
        })

        assert self.test_object.get_option(DemoListConfigOption).value.is_list()

    def test_configure_union_type(self):
        with pytest.raises(InvalidOptionValueTypeException):
            self.test_object.configure({
                "demo_union": 123
            })

        self.test_object.configure({
            "demo_union": "hey"
        })

        assert self.test_object.get_option(DemoUnionConfigOption).value.is_str()

        self.test_object.configure({
            "demo_union": {}
        })

        assert self.test_object.get_option(DemoUnionConfigOption).value.is_dict()

    def test_configure_custom_value_type(self):
        with pytest.raises(InvalidOptionValueTypeException):
            self.test_object.configure({
                "demo_custom_value": CustomTypeConfigValue(raw=123)
            })

        self.test_object.configure({
            "demo_custom_value": CustomTypeConfigValue(raw="yeah")
        })

        assert self.test_object.get_option(DemoCustomValueConfigOption).value.is_str()

    def test_configure_nested_dict_type(self):
        self.test_object.configure({
            "demo_dict": {
                "lorem": "ipsum",
                "dolor": ["sit"],
                "amet": {
                    "this_is_a_bool": True,
                    "this_is_an_int": 123
                }
            }
        })

        assert self.test_object.get_option(DemoDictConfigOption).value.is_dict()
