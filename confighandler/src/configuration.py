from typing import Any
from ._functions import get_config, ConfigurationModel


class Configuration:
    """
    Class to encapsulate the configuration settings for the entire application.
    """

    def __init__(
        self,
        appname: str = "",
        debugging: bool = False,
        named_attributes: bool = False,
        ini_file: str = "database.ini",
    ):
        self.named_attributes = named_attributes
        self.initialized = True
        self.ini_file = ini_file
        self.validation_model = ConfigurationModel(
            appname=appname, debugging=debugging, ini_file=self.ini_file
        )
        self.configs: dict = get_config(
            appname=appname, debugging=debugging, ini_file=self.ini_file
        )

    def __getattr__(self, name: str) -> Any:
        """
        Enables direct attribute access to config-values

        **Args:**
            **name** (*str*): The name of the attribute
        """
        if name in self.configs:
            return self.configs[name]
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")

    def __dir__(self) -> list[str]:
        """
        Returns list of valid attributes including config keys.
        Enables runtime attribute discovery and IDE autocompletion.
        """
        # Combine standard attributes with config keys
        standard_attrs = list(super().__dir__())
        config_attrs = list(self.configs.keys())
        return sorted(set(standard_attrs + config_attrs))
