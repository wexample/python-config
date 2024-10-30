import pytest

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
