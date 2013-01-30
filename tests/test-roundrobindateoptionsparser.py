# -*- coding: utf8 -*-

# nosetests --with-coverage --cover-package=roundrobindate ./tests

from nose.tools import *
from roundrobindate import RoundRobinDateOptionsParser
from datetime import date

class TestRoundRobinDateOptionsParser():

    def setup(self):
        "Set up test fixtures"
        self.options_parser = RoundRobinDateOptionsParser()

    def teardown(self):
        "Tear down test fixtures"

    def test_set_option_single_value(self):
        "Test setting a single option value"
        default_options = self.options_parser.get_options()
        new_day_value = 8
        self.options_parser.set_options({"days_to_retain": new_day_value})
        result = self.options_parser.get_options()
        assert_equal(result.get("days_to_retain"), new_day_value)
        assert_equal(
            result.get("years_to_retain"),
            default_options.get("years_to_retain"),
            "Ensure other option values are not accidentally changed too"
        )

    def test_set_option_string_start_date(self):
        "Test setting start date as string"
        new_start_date_value = {"start_date": "20101105"}
        expected_parsed_result = date(2010, 11, 05)
        self.options_parser.set_options(new_start_date_value)
        returned_options = self.options_parser.get_options()
        returned_start_date_value = returned_options.get("start_date")
        assert_equal(returned_start_date_value, expected_parsed_result)

    def test_set_option_all_values(self):
        "Test setting all options"
        new_options = {
            "start_date": date.today(),
            "days_to_retain": 8,
            "weeks_to_retain": 4,
            "months_to_retain": 7,
            "years_to_retain": 0
        }
        self.options_parser.set_options(new_options)
        result = self.options_parser.get_options()
        assert_equal(result, new_options)

    def test_default_options(self):
        "Test the default options"
        self.test_set_option_all_values()
        self.options_parser.set_default_options()
        expected = self.options_parser._get_default_options()
        result = self.options_parser.get_options()
        assert_equal(result, expected)
