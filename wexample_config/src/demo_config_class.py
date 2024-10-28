from typing import List, Type
from typing_extensions import TYPE_CHECKING
from wexample_config.classes.mixins.multiple_options_providers_mixin import MultipleOptionsProvidersMixin
from wexample_config.options_provider.demo_options_provider import DemoOptionsProvider

if TYPE_CHECKING:
    from wexample_config.options_provider.abstract_options_provider import AbstractOptionsProvider


class DemoConfigClass(MultipleOptionsProvidersMixin):
    def get_options_providers(self) -> List[Type["AbstractOptionsProvider"]]:
        return [
            DemoOptionsProvider,
        ]