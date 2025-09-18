from unittest import TestCase
from pydantic import ValidationError
from confighandler.src._functions import get_parameter, load_config



class TestMissingCols(TestCase):
    def setUp(self) -> None:
        self.valid_app_name: str = "nk-edoc-geocoding"
        self.config = load_config("/Users/madsd/Desktop/git/_dev/database.ini")
        self.invalid_row = {
            'id':'temp',
            'name':'name1',
            'description':'desc1',
            'type_id': '2',
            'value':1,
            #'debugmode': # no debug mode
        }


    def test_missing_col(self) -> None:
        """
        Testing if a missing column will throw an error
        """
        with self.assertRaises(ValueError):
            get_parameter(self.invalid_row)