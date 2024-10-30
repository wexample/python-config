
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, Union, cast

from wexample_config.option.abstract_config_option import AbstractConfigOption


class AbstractNestedConfigOption(AbstractConfigOption):
    options: Dict[str, AbstractConfigOption] = {}
    pass
