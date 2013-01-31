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
        new_start_date_value = {"start_date": "2010-11-05"}
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

    def test_get_dates_with_no_retain_options(self):
        new_options = {
            "days_to_retain": 0,
            "weeks_to_retain": 0,
            "months_to_retain": 0,
            "years_to_retain": 0
        }
        self.rrd.set_options(new_options)

        expected = {}
        result = self.rrd.get_dates()
        assert_equal(result, expected)

        expected = {}
        result = self.rrd.get_dates(direction="future")
        assert_equal(result, expected)

    def test_get_dates_future_with_retain_days_options(self):
        new_options = {
            "start_date": "2010-12-30",
            "days_to_retain": 3,
            "weeks_to_retain": 0,
            "months_to_retain": 0,
            "years_to_retain": 0
        }
        self.rrd.set_options(new_options)

        expected = {
            "2010-12-30": date(2010, 12, 30),
            "2010-12-31": date(2010, 12, 31),
            "2011-01-01": date(2011, 1, 1),
        }
        result = self.rrd.get_dates(direction="future")
        assert_equal(result, expected)

    def test_get_dates_as_strings_past_with_retain_days_options(self):
        new_options = {
            "start_date": "2011-01-01",
            "days_to_retain": 3,
            "weeks_to_retain": 0,
            "months_to_retain": 0,
            "years_to_retain": 0
        }
        self.rrd.set_options(new_options)

        expected = ["2011-01-01", "2010-12-31", "2010-12-30"]
        result = self.rrd.get_dates_as_strings()
        assert_equal(result, expected)

    def test_get_dates_as_strings_future_with_retain_days_options(self):
        new_options = {
            "start_date": "2010-12-30",
            "days_to_retain": 3,
            "weeks_to_retain": 0,
            "months_to_retain": 0,
            "years_to_retain": 0
        }
        self.rrd.set_options(new_options)

        expected = ["2010-12-30", "2010-12-31", "2011-01-01"]
        result = self.rrd.get_dates_as_strings(direction="future")
        assert_equal(result, expected)

    def test_get_dates_past_with_retain_weeks_options(self):
        new_options = {
            "start_date": "2012-01-01",
            "days_to_retain": 0,
            "weeks_to_retain": 2,
            "months_to_retain": 0,
            "years_to_retain": 0
        }
        self.rrd.set_options(new_options)

        expected = {
            "2011-12-25": date(2011, 12, 25),
            "2011-12-18": date(2011, 12, 18),
        }
        result = self.rrd.get_dates()
        assert_equal(result, expected)

    def test_get_dates_future_with_retain_weeks_options(self):
        new_options = {
            "start_date": "2010-12-30",
            "days_to_retain": 0,
            "weeks_to_retain": 2,
            "months_to_retain": 0,
            "years_to_retain": 0
        }
        self.rrd.set_options(new_options)

        expected = {
            "2011-01-06": date(2011, 1, 6),
            "2011-01-13": date(2011, 1, 13),
        }
        result = self.rrd.get_dates(direction="future")
        assert_equal(result, expected)

    def test_get_dates_past_with_retain_months_options(self):
        new_options = {
            "start_date": "2012-02-29",
            "days_to_retain": 0,
            "weeks_to_retain": 0,
            "months_to_retain": 6,
            "years_to_retain": 0
        }
        self.rrd.set_options(new_options)

        expected = {
            "2012-01-28": date(2012, 1, 28),
            "2011-12-28": date(2011, 12, 28),
            "2011-11-28": date(2011, 11, 28),
            "2011-10-28": date(2011, 10, 28),
            "2011-09-28": date(2011, 9, 28),
            "2011-08-28": date(2011, 8, 28)
        }
        result = self.rrd.get_dates()
        assert_equal(result, expected)

    def test_get_dates_future_with_retain_months_options(self):
        new_options = {
            "start_date": "2012-02-29",
            "days_to_retain": 0,
            "weeks_to_retain": 0,
            "months_to_retain": 6,
            "years_to_retain": 0
        }
        self.rrd.set_options(new_options)

        expected = {
            "2012-03-28": date(2012, 3, 28),
            "2012-04-28": date(2012, 4, 28),
            "2012-05-28": date(2012, 5, 28),
            "2012-06-28": date(2012, 6, 28),
            "2012-07-28": date(2012, 7, 28),
            "2012-08-28": date(2012, 8, 28)
        }
        result = self.rrd.get_dates(direction="future")
        assert_equal(result, expected)

    def test_get_dates_past_with_retain_years_options(self):
        new_options = {
            "start_date": "2012-02-29",
            "days_to_retain": 0,
            "weeks_to_retain": 0,
            "months_to_retain": 0,
            "years_to_retain": 5
        }
        self.rrd.set_options(new_options)

        expected = {
            "2011-02-28": date(2011, 2, 28),
            "2010-02-28": date(2010, 2, 28),
            "2009-02-28": date(2009, 2, 28),
            "2008-02-28": date(2008, 2, 28),
            "2007-02-28": date(2007, 2, 28),
        }
        result = self.rrd.get_dates()
        assert_equal(result, expected)

    def test_get_dates_future_with_retain_years_options(self):
        new_options = {
            "start_date": "2012-02-29",
            "days_to_retain": 0,
            "weeks_to_retain": 0,
            "months_to_retain": 0,
            "years_to_retain": 5
        }
        self.rrd.set_options(new_options)

        expected = {
            "2013-02-28": date(2013, 2, 28),
            "2014-02-28": date(2014, 2, 28),
            "2015-02-28": date(2015, 2, 28),
            "2016-02-28": date(2016, 2, 28),
            "2017-02-28": date(2017, 2, 28),
        }
        result = self.rrd.get_dates(direction="future")
        assert_equal(result, expected)

    def test_get_dates_as_strings_past_with_day_and_week_retain_options(self):
        "Test overlapping dates collapse"
        new_options = {
            "start_date": "2012-02-29",
            "days_to_retain": 9,
            "weeks_to_retain": 1,
            "months_to_retain": 0,
            "years_to_retain": 0
        }
        self.rrd.set_options(new_options)

        expected = [
            "2012-02-29",
            "2012-02-28",
            "2012-02-27",
            "2012-02-26",
            "2012-02-25",
            "2012-02-24",
            "2012-02-23",
            "2012-02-22",
            "2012-02-21"
        ]
        result = self.rrd.get_dates_as_strings()
        assert_equal(result, expected)

    def test_get_dates_as_strings_future_with_day_and_week_retain_options(self):
        "Test overlapping dates collapse"
        new_options = {
            "start_date": "2012-02-29",
            "days_to_retain": 9,
            "weeks_to_retain": 1,
            "months_to_retain": 0,
            "years_to_retain": 0
        }
        self.rrd.set_options(new_options)

        expected = [
            "2012-02-29",
            "2012-03-01",
            "2012-03-02",
            "2012-03-03",
            "2012-03-04",
            "2012-03-05",
            "2012-03-06",
            "2012-03-07",
            "2012-03-08"
        ]
        result = self.rrd.get_dates_as_strings(direction="future")
        assert_equal(result, expected)

    def test_get_dates_as_strings_past_with_week_and_month_retain_options(self):
        "Illustrate week and month boundaries do not necessarily overlap"
        new_options = {
            "start_date": "2012-01-01",
            "days_to_retain": 0,
            "weeks_to_retain": 5,
            "months_to_retain": 1,
            "years_to_retain": 0
        }
        self.rrd.set_options(new_options)

        expected = [
            "2011-12-25",
            "2011-12-18",
            "2011-12-11",
            "2011-12-04",
            "2011-12-01",
            "2011-11-27",
        ]
        result = self.rrd.get_dates_as_strings()
        assert_equal(result, expected)

    def test_get_dates_as_strings_future_with_week_and_month_retain_options(self):
        "Illustrate week and month boundaries do not necessarily overlap"
        new_options = {
            "start_date": "2012-01-01",
            "days_to_retain": 0,
            "weeks_to_retain": 5,
            "months_to_retain": 1,
            "years_to_retain": 0
        }
        self.rrd.set_options(new_options)

        expected = [
            "2012-01-08",
            "2012-01-15",
            "2012-01-22",
            "2012-01-29",
            "2012-02-01",
            "2012-02-05",
        ]
        result = self.rrd.get_dates_as_strings(direction="future")
        assert_equal(result, expected)

    def test_get_dates_past_with_all_options(self):
        new_options = {
            "start_date": "2012-02-29",
            "days_to_retain": 1,
            "weeks_to_retain": 1,
            "months_to_retain": 1,
            "years_to_retain": 1
        }
        self.rrd.set_options(new_options)

        expected = {
            "2012-02-29": date(2012, 2, 29),
            "2012-02-22": date(2012, 2, 22),
            "2012-01-28": date(2012, 1, 28),
            "2011-02-28": date(2011, 2, 28),
        }
        result = self.rrd.get_dates()
        unordered_result = dict(result)
        assert_equal(unordered_result, expected)

    def test_get_dates_future_with_all_options(self):
        new_options = {
            "start_date": "2012-02-29",
            "days_to_retain": 1,
            "weeks_to_retain": 1,
            "months_to_retain": 1,
            "years_to_retain": 1
        }
        self.rrd.set_options(new_options)

        expected = {
            "2012-02-29": date(2012, 2, 29),
            "2012-03-07": date(2012, 3, 7),
            "2012-03-28": date(2012, 3, 28),
            "2013-02-28": date(2013, 2, 28),
        }
        result = self.rrd.get_dates(direction="future")
        unordered_result = dict(result)
        assert_equal(unordered_result, expected)
