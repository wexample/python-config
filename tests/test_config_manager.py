import pytest
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
