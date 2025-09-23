from unittest import TestCase
from confighandler.src.configuration import Configuration

class TestDunder(TestCase):
    def setUp(self) -> None:
        self.valid_app_name = "nk-edoc-geocoding"
        self.valid_debug = False
        self.config = Configuration(
            self.valid_app_name,
            self.valid_debug,
            ini_file="/Users/madsd/Desktop/git/_dev/database.ini",
        )

    def test_get_valid_attr(self):
        """
        Testing if it's able to access an attribute we know exists
        """
        self.assertTrue(self.config.table_name)

    def test_invalid_attr(self):
        """
        Testing if correctly raises returns False, when we don't have a given attribute
        """
        with self.assertRaises(AttributeError):
            self.config.random_attr

    def test_get_repr(self):
        self.assertIsInstance(repr(self.config), str)
        print(repr(self.config))

    def test_get_dir(self):
        self.assertIsInstance(self.config.__dir__(), list)
        print(dir(self.config))