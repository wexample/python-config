from typing import List, Type, TYPE_CHECKING

from wexample_config.demo.config_option.demo_list_config_option import DemoListConfigOption
from wexample_config.options_provider.abstract_options_provider import AbstractOptionsProvider

if TYPE_CHECKING:
    from wexample_config.config_option.abstract_config_option import AbstractConfigOption


class DemoOptionsProvider(AbstractOptionsProvider):
    @classmethod
    def get_options(cls) -> List[Type["AbstractConfigOption"]]:
        from wexample_config.config_option.name_config_option import NameConfigOption

        return [
            DemoListConfigOption,
            NameConfigOption,
        ]
