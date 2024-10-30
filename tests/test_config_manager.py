import pytest

from wexample_config.src.demo_config_class import DemoConfigClass


class TestConfigManager:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.config_manager = DemoConfigClass()

    def test_setup(self):
        assert self.config_manager is not None
