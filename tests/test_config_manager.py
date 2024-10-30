import pytest

from wexample_config.config_value.custom_type_config_value import CustomTypeConfigValue
from wexample_config.demo.config_option.demo_custom_value_config_option import DemoCustomValueConfigOption
from wexample_config.demo.config_option.demo_extensible_config_option import DemoExtensibleConfigOption
from wexample_config.demo.config_option.demo_union_config_option import DemoUnionConfigOption
from wexample_config.demo.demo_config_manager import DemoConfigManager
from wexample_config.exception.option import InvalidOptionException, InvalidOptionValueTypeException
from wexample_config.config_option.name_config_option import NameConfigOption
from wexample_config.demo.config_option.demo_list_config_option import DemoListConfigOption


class TestConfigManager:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.config_manager = DemoConfigManager()

    def test_setup(self):
        assert isinstance(self.config_manager, DemoConfigManager)

    def test_configure_name(self):
        self.config_manager.set_value({
            "name": "yes"
        })

        assert self.config_manager.value.is_dict()
        assert self.config_manager.get_name() == "demo_config_manager"
        assert len(self.config_manager.options)
        assert self.config_manager.get_option("name").value.is_str()
        assert self.config_manager.get_option(NameConfigOption).value.is_str()

    def test_configure_unexpected(self):
        with pytest.raises(InvalidOptionException):
            self.config_manager.set_value({
                "unexpected_option": "yes"
            })

    def test_configure_unexpected_type(self):
        with pytest.raises(InvalidOptionValueTypeException):
            self.config_manager.set_value({
                "name": 123
            })

        with pytest.raises(InvalidOptionValueTypeException):
            self.config_manager.set_value({
                "name": []
            })

    def test_configure_list_type(self):
        with pytest.raises(InvalidOptionValueTypeException):
            self.config_manager.set_value({
                "demo_list": 123
            })

        self.config_manager.set_value({
            "demo_list": []
        })

        assert self.config_manager.get_option(DemoListConfigOption).value.is_list()

    def test_configure_union_type(self):
        with pytest.raises(InvalidOptionValueTypeException):
            self.config_manager.set_value({
                "demo_union": 123
            })

        self.config_manager.set_value({
            "demo_union": "hey"
        })

        assert self.config_manager.get_option(DemoUnionConfigOption).value.is_str()

        self.config_manager.set_value({
            "demo_union": {}
        })

        assert self.config_manager.get_option(DemoUnionConfigOption).value.is_dict()

    def test_configure_custom_value_type(self):
        with pytest.raises(InvalidOptionValueTypeException):
            self.config_manager.set_value({
                "demo_custom_value": CustomTypeConfigValue(raw=123)
            })

        self.config_manager.set_value({
            "demo_custom_value": CustomTypeConfigValue(raw="yeah")
        })

        assert self.config_manager.get_option(DemoCustomValueConfigOption).value.is_str()
        assert self.config_manager.get_option(DemoCustomValueConfigOption).value.get_str() == "yeah"

    def test_configure_extensible(self):
        # Extensible children option
        self.config_manager.set_value({
            "demo_extensible": {
                "unexpected_option": "yes",
                "unexpected_dict": {
                    "unexpected_option": "yay",
                }
            }
        })

        assert self.config_manager.get_option(DemoExtensibleConfigOption).value.is_dict()

        # Unexpected option fails on current
        with pytest.raises(InvalidOptionException):
            self.config_manager.set_value({
                "lorem": "ipsum"
            })

        # Works if configured
        self.config_manager.allow_undefined_keys = True
        self.config_manager.set_value({
            "lorem": "ipsum"
        })

        # In nested, unexpected keys for child are still not allowed, if not specified in class handler.
        with pytest.raises(InvalidOptionException):
            self.config_manager.allow_undefined_keys = True
            self.config_manager.set_value({
                "demo_nested": {
                    "lorem": "ipsum"
                }
            })

        self.config_manager.allow_undefined_keys = False
