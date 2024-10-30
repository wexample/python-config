import pytest

from wexample_config.config_value.custom_type_config_value import CustomTypeConfigValue
from wexample_config.option.demo_custom_value_config_option import DemoCustomValueConfigOption
from wexample_config.option.demo_dict_config_option import DemoDictConfigOption
from wexample_config.option.demo_extensible_config_option import DemoExtensibleConfigOption
from wexample_config.option.demo_list_config_option import DemoListConfigOption
from wexample_config.option.demo_nested_config_option import DemoNestedConfigOption
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
        self.test_object.set_value({
            "name": "yes"
        })

    def test_configure_unexpected(self):
        with pytest.raises(InvalidOptionException):
            self.test_object.set_value({
                "unexpected_option": "yes"
            })

    def test_configure_unexpected_type(self):
        with pytest.raises(InvalidOptionValueTypeException):
            self.test_object.set_value({
                "name": 123
            })

        with pytest.raises(InvalidOptionValueTypeException):
            self.test_object.set_value({
                "name": []
            })

    def test_configure_list_type(self):
        with pytest.raises(InvalidOptionValueTypeException):
            self.test_object.set_value({
                "demo_list": 123
            })

        self.test_object.set_value({
            "demo_list": []
        })

        assert self.test_object.get_option(DemoListConfigOption).value.is_list()

    def test_configure_union_type(self):
        with pytest.raises(InvalidOptionValueTypeException):
            self.test_object.set_value({
                "demo_union": 123
            })

        self.test_object.set_value({
            "demo_union": "hey"
        })

        assert self.test_object.get_option(DemoUnionConfigOption).value.is_str()

        self.test_object.set_value({
            "demo_union": {}
        })

        assert self.test_object.get_option(DemoUnionConfigOption).value.is_dict()

    def test_configure_custom_value_type(self):
        with pytest.raises(InvalidOptionValueTypeException):
            self.test_object.set_value({
                "demo_custom_value": CustomTypeConfigValue(raw=123)
            })

        self.test_object.set_value({
            "demo_custom_value": CustomTypeConfigValue(raw="yeah")
        })

        assert self.test_object.get_option(DemoCustomValueConfigOption).value.is_str()

    def test_configure_name(self):
        # Extensible children option
        self.test_object.set_value({
            "demo_extensible": {
                "unexpected_option": "yes",
                "unexpected_dict": {
                    "unexpected_option": "yay",
                }
            }
        })

        assert self.test_object.get_option(DemoExtensibleConfigOption).value.is_dict()

        # Unexpected option fails on current
        with pytest.raises(InvalidOptionException):
            self.test_object.set_value({
                "lorem": "ipsum"
            })

        # Works if configured
        self.test_object.allow_undefined_keys = True
        self.test_object.set_value({
            "lorem": "ipsum"
        })

        # In nested, unexpected keys for child are still not allowed, if not specified in class handler.
        with pytest.raises(InvalidOptionException):
            self.test_object.allow_undefined_keys = True
            self.test_object.nested = True
            self.test_object.set_value({
                "demo_nested": {
                    "lorem": "ipsum"
                }
            })

        self.test_object.nested = False
        self.test_object.allow_undefined_keys = False

    def test_configure_nested_dict_type(self):
        self.test_object.set_value(
            {
                "demo_nested": {
                    "name": "FIRST_LEVEL_DICT",
                    "demo_dict": {
                        "lorem": {
                            "info": "As the demo_dict is typed, we should have sub dicts"
                                    "the type is like: Dict[str, Dict[str, Any]]",
                            "other": 123
                        },
                        #     #     "demo_custom_value": CustomTypeConfigValue(raw="yeah")
                    }
                }
            }
        )

        # Main dict is saved
        assert isinstance(self.test_object.value.get_dict(), dict)

        option = self.test_object.get_option(DemoNestedConfigOption)
        assert isinstance(option, DemoNestedConfigOption)

        # Sub class has been created
        option = self.test_object.get_option_recursive(DemoDictConfigOption)

        assert isinstance(option, DemoDictConfigOption)
        assert isinstance(option.value.get_dict().get("lorem"), dict)

