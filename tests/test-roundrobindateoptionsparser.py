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

    def test_set_option_current_date_object(self):
        "Test setting current date with date object"
        current_date = date(2010, 11, 05)
        new_option = {"current_date": current_date}
        self.options_parser.set_options(new_option)
        returned_options = self.options_parser.get_options()
        option_value = returned_options.get("current_date")
        assert_equal(option_value, current_date)

    def test_set_option_current_date_string(self):
        "Test setting current date with date strings"
        current_date_string = "2010-11-05"
        expected = date(2010, 11, 05)
        new_options = {"current_date": current_date_string}
        self.options_parser.set_options(new_options)
        returned_options = self.options_parser.get_options()
        option_value = returned_options.get("current_date")
        assert_equal(option_value, expected)

        current_date_string = "2010.11.05"
        expected = date(2010, 11, 05)
        new_options = {"current_date": current_date_string}
        self.options_parser.set_options(new_options)
        returned_options = self.options_parser.get_options()
        option_value = returned_options.get("current_date")
        assert_equal(option_value, expected)

    def test_set_option_anchor_date(self):
        "Test setting anchor date with date object and date string"
        anchor_date = date(2010, 11, 05)
        new_option = {"anchor_date": anchor_date}
        self.options_parser.set_options(new_option)
        returned_options = self.options_parser.get_options()
        option_value = returned_options.get("anchor_date")
        assert_equal(option_value, anchor_date)

        anchor_date_string = "2010-11-05"
        expected = date(2010, 11, 05)
        new_option = {"anchor_date": anchor_date_string}
        self.options_parser.set_options(new_option)
        returned_options = self.options_parser.get_options()
        option_value = returned_options.get("anchor_date")
        assert_equal(option_value, expected)

    def test_set_option_anchor_date_and_confirm_backup_days_set(self):
        "Set new anchor date and confirm backup days are set based off of it"
        anchor_date = date(2010, 11, 05)
        new_option = {"anchor_date": anchor_date}
        day_of_week = anchor_date.isoweekday()
        day_of_month = anchor_date.day
        month_of_year = anchor_date.month
        self.options_parser.set_options(new_option)
        returned = self.options_parser.get_options()
        assert_equal(returned.get("backup_day_of_week"), day_of_week)
        assert_equal(returned.get("backup_day_of_month"), day_of_month)
        assert_equal(returned.get("backup_month_of_year"), month_of_year)

    def test_set_option_anchor_date_late_in_month_and_confirm_backup_days_set(self):
        """
        Notice backup day of the month can't be higher to 28, will auto adjust.
        """
        anchor_date = date(2010, 11, 30)
        new_option = {"anchor_date": anchor_date}
        day_of_month = 28
        self.options_parser.set_options(new_option)
        returned = self.options_parser.get_options()
        assert_equal(returned.get("backup_day_of_month"), day_of_month)

    def test_set_option_all_values(self):
        "Test setting all options"
        new_options = {
            "current_date": date(2011, 1, 1),
            "anchor_date": None,
            "backup_day_of_week": 0,
            "backup_day_of_month": 1,
            "backup_month_of_year": 1,
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
