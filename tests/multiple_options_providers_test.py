import unittest


class MultipleOptionsProvidersTest(unittest.TestCase):
    def setUp(self):
        from wexample_config.src.demo_config_class import DemoConfigClass

        self.test_object = DemoConfigClass()

    def test_setup(self):
        self.assertIsNotNone(
            self.test_object
        )

    def test_configure_name(self):
        self.test_object.configure({
            "name": "yes"
        })

    def test_configure_unexpected(self):
        from wexample_config.exception.option import InvalidOptionException

        with self.assertRaises(InvalidOptionException):
            self.test_object.configure({
                "unexpected_option": "yes"
            })

    def test_configure_unexpected_type(self):
        from wexample_config.exception.option import InvalidOptionValueTypeException

        with self.assertRaises(InvalidOptionValueTypeException):
            self.test_object.configure({
                "name": 123
            })

        with self.assertRaises(InvalidOptionValueTypeException):
            self.test_object.configure({
                "name": []
            })
