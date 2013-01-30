# -*- coding: utf8 -*-

# nosetests --with-coverage --cover-package=roundrobindate ./tests

from nose.tools import *
from roundrobindate import RoundRobinDate
from datetime import date

class RoundRobinDateTestingChild(RoundRobinDate):
    """
    Identical to RoundRobinDate with additional ability to manipulate the date
    value.
    """
    def __init__(self, options=""):
        RoundRobinDate.__init__(self, options)

    def _get_current_date(self):
        " Abstracted current date to aid testing by inheritence. "
        return self._testing_date

    def set_current_date(self, year, month, day):
        self._testing_date = date(year, month, day)

class TestRoundRobinDate():

    def setup(self):
        "Set up test fixtures"
        self.rrd = RoundRobinDateTestingChild()

    def teardown(self):
        "Tear down test fixtures"

    def test_set_current_date(self):
        self.rrd.set_current_date(2010,01,05)
        result = self.rrd._get_current_date()
        assert_equal(result.day, 5)
        assert_equal(result.month, 1)
        assert_equal(result.year, 2010)

    def test__get_next_month(self):
        expected = 2
        result = self.rrd._get_next_month(1)
        assert_equal(result, expected)

        expected = 1
        result = self.rrd._get_next_month(12)
        assert_equal(result, expected)

    def test__get_days_in_month(self):
        result = self.rrd._get_days_in_month(1, 2010)
        assert_equal(result, 31, "Testing 31 day month")

        result = self.rrd._get_days_in_month(4, 2010)
        assert_equal(result, 30, "Testing 30 day month")

        result = self.rrd._get_days_in_month(2, 2010)
        assert_equal(result, 28, "Testing non-leap year")

        result = self.rrd._get_days_in_month(2, 2012)
        assert_equal(result, 29, "Testing leap year")

        try:
            result = self.rrd._get_days_in_month("4", "2010")
            assert False
        except TypeError:
            assert True

    def test__get_current_date(self):
        """
        For testing purposes the original method is overwritten in the child
        testing class. This tests the original method.
        """
        original_rrd = RoundRobinDate()
        expected = date.today()
        result = original_rrd._get_current_date()
        assert_equal(result, expected)

    def test_set_option_single_value(self):
        "Test setting a single option value"
        default_options = self.rrd.get_options()
        new_day_value = 8
        self.rrd.set_options({"days_to_retain": new_day_value})
        result = self.rrd.get_options()
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
        self.rrd.set_options(new_start_date_value)
        returned_options = self.rrd.get_options()
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
        self.rrd.set_options(new_options)
        result = self.rrd.get_options()
        assert_equal(result, new_options)

