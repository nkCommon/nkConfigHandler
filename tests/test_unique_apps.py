from unittest import TestCase
from pydantic import ValidationError
from confighandler.src._functions import ConfigurationModel, get_unique_app_names



class TestUniqueApps(TestCase):
    def setUp(self) -> None:
        self.valid_app_name: str = "nk-edoc-geocoding"
        self.invalid_app_name: str = "mit-mega-seje-program"
        self.too_short: str = "kort"
        self.invalid_debug: str = "False"
        self.valid_debug: bool = False

    def test_all_apps(self) -> None:
        """
        Testing if it returns a set
        """
        self.apps = get_unique_app_names("/Users/madsd/Desktop/git/_dev/database.ini")
        self.assertIsInstance(self.apps, set)
        # self.assertIsInstance(get_unique_app_names().pop(), str)

    def test_invalid_app_name(self) -> None:
        """
        Testing if it raises an error for an invalid app name
        """
        with self.assertRaises(ValidationError):
            ConfigurationModel(
                appname=self.invalid_app_name,
                debugging=False,
                ini_file="/Users/madsd/Desktop/git/_dev/database.ini",
            )

    def test_valid_app_name(self) -> None:
        """
        Testing if it accepts a valid app name
        """
        validation_model = ConfigurationModel(
            appname=self.valid_app_name,
            debugging=False,
            ini_file="/Users/madsd/Desktop/git/_dev/database.ini",
        )
        self.assertEqual(validation_model.appname, self.valid_app_name)
        self.assertEqual(validation_model.debugging, False)

    def test_too_short_app_name(self) -> None:
        """
        Testing if it raises an error for an app name that's too short
        """
        with self.assertRaises(ValidationError):
            ConfigurationModel(
                appname=self.too_short, debugging=False
            )

    def test_wrong_input(self) -> None:
        """
        Testing, if it throws an error on invalid input-types
        """
        with self.assertRaises(ValidationError):
            ConfigurationModel(
                appname=1,
                debugging=True,
                ini_file="/Users/madsd/Desktop/git/_dev/database.ini",
            )

        with self.assertRaises(ValidationError):
            ConfigurationModel(
                appname="testApp",
                debugging="Ja",
                ini_file="/Users/madsd/Desktop/git/_dev/database.ini",
            )

        with self.assertRaises(ValidationError):
            ConfigurationModel(
                appname="testApp",
                debugging="True",
                ini_file="/Users/madsd/Desktop/git/_dev/database.ini",
            )

        with self.assertRaises(ValidationError):
            ConfigurationModel(appname="testApp", debugging=True, ini_file=1)
