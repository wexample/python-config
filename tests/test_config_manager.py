import pytest

from wexample_config.demo.demo_config_manager import DemoConfigManager


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
