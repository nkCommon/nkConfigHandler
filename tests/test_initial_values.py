from unittest import TestCase
from pydantic import ValidationError
from confighandler.src.configuration import Configuration
from confighandler.src._functions import get_parameter, load_config

class TestConfiguration(TestCase):
    def setUp(self) -> None:
        self.valid_app_name = "nk-edoc-geocoding"
        self.invalid_app_name = "mit-mega-seje-program"
        self.too_short = "kort"
        self.invalid_debug = "False"
        self.valid_debug = False
        self.config: Configuration
        self.invalid_type = {
            'id':'temp',
            'name':'name1',
            'description':'desc1',
            'type_id': '2',
            'value':"1",
            'debugmode': True
        }

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

    def test_invalid_value(self):
        with self.assertRaises(ValueError):
            config = load_config("/Users/madsd/Desktop/git/_dev/database.ini")
            get_parameter(self.invalid_type)

