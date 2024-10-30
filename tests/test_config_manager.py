import pytest

from wexample_config.demo.demo_config_manager import DemoConfigManager


class TestConfigManager:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.config_manager = DemoConfigManager()

    def test_setup(self):
        assert self.config_manager is not None
