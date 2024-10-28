from wexample_config.config_value.config_value import ConfigValue


class StringConfigValue(ConfigValue):
    @staticmethod
    def get_value_type() -> type:
        return str
