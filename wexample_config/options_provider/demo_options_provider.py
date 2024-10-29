from typing import List, Type, TYPE_CHECKING

from wexample_config.option.demo_list_config_option import DemoListConfigOption
from wexample_config.option.demo_union_config_option import DemoUnionConfigOption
from wexample_config.options_provider.abstract_options_provider import AbstractOptionsProvider

if TYPE_CHECKING:
    from wexample_config.option.abstract_config_option import AbstractConfigOption


class DemoOptionsProvider(AbstractOptionsProvider):
    @classmethod
    def get_options(cls) -> List[Type["AbstractConfigOption"]]:
        from wexample_config.option.name_config_option import NameConfigOption

        return [
            DemoListConfigOption,
            DemoUnionConfigOption,
            NameConfigOption,
        ]
