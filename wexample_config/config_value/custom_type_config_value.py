from wexample_config.config_value.config_value import ConfigValue


class CustomTypeConfigValue(ConfigValue):
    @staticmethod
    def get_allowed_types() -> type:
        return str
