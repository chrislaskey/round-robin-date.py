# -*- coding: utf8 -*-

# nosetests --with-coverage --cover-package=roundrobindate --nocapture ./tests

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

    def test_set_option_backup_day_of_week(self):
        day_of_week = 4
        new_option = {"backup_day_of_week": day_of_week}
        self.options_parser.set_options(new_option)
        returned_options = self.options_parser.get_options()
        option_value = returned_options.get("backup_day_of_week")
        assert_equal(option_value, day_of_week)

        day_of_week = "4"
        new_option = {"backup_day_of_week": day_of_week}
        self.options_parser.set_options(new_option)
        returned_options = self.options_parser.get_options()
        option_value = returned_options.get("backup_day_of_week")
        assert_equal(option_value, int(day_of_week))

        def invalid_input_zero():
            new_option = {"backup_day_of_week": 0}
            self.options_parser.set_options(new_option)
        assert_raises(Exception, invalid_input_zero)

        def invalid_input_too_high():
            new_option = {"backup_day_of_week": 8}
            self.options_parser.set_options(new_option)
        assert_raises(Exception, invalid_input_zero)

    def test_set_option_backup_day_of_month(self):
        day_of_month = 22
        new_option = {"backup_day_of_month": day_of_month}
        self.options_parser.set_options(new_option)
        returned_options = self.options_parser.get_options()
        option_value = returned_options.get("backup_day_of_month")
        assert_equal(option_value, day_of_month)

        day_of_month = "22"
        new_option = {"backup_day_of_month": day_of_month}
        self.options_parser.set_options(new_option)
        returned_options = self.options_parser.get_options()
        option_value = returned_options.get("backup_day_of_month")
        assert_equal(option_value, int(day_of_month))

        def invalid_input_zero():
            new_option = {"backup_day_of_month": 0}
            self.options_parser.set_options(new_option)
        assert_raises(Exception, invalid_input_zero)

        def invalid_input_too_high():
            new_option = {"backup_day_of_month": 32}
            self.options_parser.set_options(new_option)
        assert_raises(Exception, invalid_input_zero)

    def test_set_option_backup_month_of_year(self):
        month_of_year = 8
        new_option = {"backup_month_of_year": month_of_year}
        self.options_parser.set_options(new_option)
        returned_options = self.options_parser.get_options()
        option_value = returned_options.get("backup_month_of_year")
        assert_equal(option_value, month_of_year)

        month_of_year = "8"
        new_option = {"backup_month_of_year": month_of_year}
        self.options_parser.set_options(new_option)
        returned_options = self.options_parser.get_options()
        option_value = returned_options.get("backup_month_of_year")
        assert_equal(option_value, int(month_of_year))

        def invalid_input_zero():
            new_option = {"backup_month_of_year": 0}
            self.options_parser.set_options(new_option)
        assert_raises(Exception, invalid_input_zero)

        def invalid_input_too_high():
            new_option = {"backup_month_of_year": 13}
            self.options_parser.set_options(new_option)
        assert_raises(Exception, invalid_input_zero)

    def test_set_option_anchor_date_takes_precendence_over_backup_day_options(self):
        """
        When an anchor day is set, it takes precedence over any backup
        day options.
        """
        new_options = {
            "anchor_date": "2011-11-15",
            "backup_day_of_week": 1,
            "backup_day_of_month": 1,
            "backup_month_of_year": 1,
        }
        self.options_parser.set_options(new_options)
        returned = self.options_parser.get_options()
        assert_equal(returned.get("backup_day_of_week"), 2)
        assert_equal(returned.get("backup_day_of_month"), 15)
        assert_equal(returned.get("backup_month_of_year"), 11)

    def test_set_option_anchor_date_with_auto_correct(self):
        """
        Test auto date correcting when anchor date day of month is > 28.
        If so, the anchor date is moved ahead to the first of the next month.

        Useful in creating immediate backups without waiting until the day of
        the month is <= 28.

        Note: short-term the days from > 28 to < 1 will be
        backed up. In the very long term these dates will not be retained, as
        the official backup anchor date will shift to the first of the next
        month.

        The auto correct feature is most useful in automated scripts when
        the anchor_date may not be reviewed by a person before running,
        assuming the anchor_date == first day of backups.
        """
        new_options = {"anchor_date": "2011-01-31"}
        self.options_parser.set_options(new_options)
        result = self.options_parser.get_options()
        assert_equal(result.get("backup_day_of_month"), 1)
        assert_equal(result.get("backup_month_of_year"), 2)

    def test_set_option_anchor_date_without_auto_correct(self):
        def anchor_date_too_late_in_month():
            new_options = {
                "anchor_date": "2011-01-31",
                "auto_correct_backup_dates": False
            }
            self.options_parser.set_options(new_options)
        assert_raises(Exception, anchor_date_too_late_in_month)

    def test_set_option_all_values(self):
        "Test setting all options"
        new_options = {
            "current_date": date(2011, 1, 1),
            "anchor_date": None,
            "auto_correct_backup_dates": False,
            "backup_day_of_week": 1,
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
