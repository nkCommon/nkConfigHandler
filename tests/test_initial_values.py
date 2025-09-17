from unittest import TestCase
from confighandler.src.configuration import Configuration

class TestConfiguration(TestCase):
    def setUp(self) -> None:
        self.valid_app_name = "nk-edoc-geocoding"
        self.invalid_app_name = "mit-mega-seje-program"
        self.too_short = "kort"
        self.invalid_debug = "False"
        self.valid_debug = False
        self.config: Configuration

    def test_valid_app(self):
        """
        Testing if it passes correctly specified app
        """
        self.config = Configuration(
            appname=self.valid_app_name,
            debugging=self.valid_debug,
            ini_file="/Users/madsd/Desktop/git/_dev/database.ini",
        )
        self.assertIsInstance(self.config.configs, dict)
        self.assertIsInstance(self.config.edoc_pwd, str)
