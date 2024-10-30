import pytest

from wexample_config.demo.demo_config_manager import DemoConfigManager
from wexample_config.exception.option import InvalidOptionException, InvalidOptionValueTypeException


class TestConfigManager:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.config_manager = DemoConfigManager()

    def test_setup(self):
        assert isinstance(self.config_manager, DemoConfigManager)

    def test_configure_name(self):
        from wexample_config.config_option.name_config_option import NameConfigOption

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
