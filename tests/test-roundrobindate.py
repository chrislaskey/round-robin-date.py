# -*- coding: utf8 -*-

# nosetests --with-coverage --cover-package=roundrobindate ./tests

from nose.tools import *
from roundrobindate import RoundRobinDate
from datetime import date

class TestRoundRobinDate():

    def setup(self):
        "Set up test fixtures"
        self.rrd = RoundRobinDate()

    def teardown(self):
        "Tear down test fixtures"

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

    def test_get_dates_with_no_retain_options(self):
        "Always includes the current day"
        new_options = {
            "current_date": "2011-01-01",
            "days_to_retain": 0,
            "weeks_to_retain": 0,
            "months_to_retain": 0,
            "years_to_retain": 0
        }
        self.rrd.set_options(new_options)

        expected = {"2011-01-01": date(2011, 1, 1)}
        result = self.rrd.get_dates()
        assert_equal(result, expected)

    def test_get_dates_as_strings_past_with_retain_days_options(self):
        "Days to retain excludes the current day, which is always included"
        new_options = {
            "current_date": "2011-01-01",
            "days_to_retain": 3,
            "weeks_to_retain": 0,
            "months_to_retain": 0,
            "years_to_retain": 0
        }
        self.rrd.set_options(new_options)

        expected = ["2011-01-01", "2010-12-31", "2010-12-30", "2010-12-29"]
        result = self.rrd.get_dates_as_strings()
        assert_equal(result, expected)

    def test_get_dates_past_with_retain_weeks_options(self):
        new_options = {
            "current_date": "2011-01-03",
            "anchor_date": "2011-01-01",
            "days_to_retain": 0,
            "weeks_to_retain": 2,
            "months_to_retain": 0,
            "years_to_retain": 0
        }
        self.rrd.set_options(new_options)

        expected = {
            "2011-01-03": date(2011, 1, 3),
            "2011-01-01": date(2011, 1, 1),
            "2010-12-25": date(2010, 12, 25),
        }
        result = self.rrd.get_dates()
        assert_equal(result, expected)

    def test_get_dates_past_with_retain_weeks_options_with_same_anchor_and_current_dates(self):
        """
        The current day is excluded from week count. It is included in return
        values only because the current day is always returned.
        """
        new_options = {
            "current_date": "2011-01-01",
            "anchor_date": "2011-01-01",
            "days_to_retain": 0,
            "weeks_to_retain": 2,
            "months_to_retain": 0,
            "years_to_retain": 0
        }
        self.rrd.set_options(new_options)

        expected = {
            "2011-01-01": date(2011, 1, 1),
            "2010-12-25": date(2010, 12, 25),
            "2010-12-18": date(2010, 12, 18),
        }
        result = self.rrd.get_dates()
        assert_equal(result, expected)

    def test_get_dates_past_with_retain_months_options(self):
        raise Exception("Purposeful failure: class not fully implemented")
        new_options = {
            "current_date": "2012-02-01",
            "anchor_date": "2004-02-29",
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

#     def test_get_dates_past_with_retain_years_options(self):
#         new_options = {
#             "start_date": "2012-02-29",
#             "days_to_retain": 0,
#             "weeks_to_retain": 0,
#             "months_to_retain": 0,
#             "years_to_retain": 5
#         }
#         self.rrd.set_options(new_options)

#         expected = {
#             "2011-02-28": date(2011, 2, 28),
#             "2010-02-28": date(2010, 2, 28),
#             "2009-02-28": date(2009, 2, 28),
#             "2008-02-28": date(2008, 2, 28),
#             "2007-02-28": date(2007, 2, 28),
#         }
#         result = self.rrd.get_dates()
#         assert_equal(result, expected)

#     def test_get_dates_as_strings_past_with_day_and_week_retain_options(self):
#         "Test overlapping dates collapse"
#         new_options = {
#             "start_date": "2012-02-29",
#             "days_to_retain": 9,
#             "weeks_to_retain": 1,
#             "months_to_retain": 0,
#             "years_to_retain": 0
#         }
#         self.rrd.set_options(new_options)

#         expected = [
#             "2012-02-29",
#             "2012-02-28",
#             "2012-02-27",
#             "2012-02-26",
#             "2012-02-25",
#             "2012-02-24",
#             "2012-02-23",
#             "2012-02-22",
#             "2012-02-21"
#         ]
#         result = self.rrd.get_dates_as_strings()
#         assert_equal(result, expected)

#     def test_get_dates_as_strings_past_with_week_and_month_retain_options(self):
#         "Illustrate week and month boundaries do not necessarily overlap"
#         new_options = {
#             "start_date": "2012-01-01",
#             "days_to_retain": 0,
#             "weeks_to_retain": 5,
#             "months_to_retain": 1,
#             "years_to_retain": 0
#         }
#         self.rrd.set_options(new_options)

#         expected = [
#             "2011-12-25",
#             "2011-12-18",
#             "2011-12-11",
#             "2011-12-04",
#             "2011-12-01",
#             "2011-11-27",
#         ]
#         result = self.rrd.get_dates_as_strings()
#         assert_equal(result, expected)

#     def test_get_dates_past_with_all_options(self):
#         new_options = {
#             "start_date": "2012-02-29",
#             "days_to_retain": 1,
#             "weeks_to_retain": 1,
#             "months_to_retain": 1,
#             "years_to_retain": 1
#         }
#         self.rrd.set_options(new_options)

#         expected = {
#             "2012-02-29": date(2012, 2, 29),
#             "2012-02-22": date(2012, 2, 22),
#             "2012-01-28": date(2012, 1, 28),
#             "2011-02-28": date(2011, 2, 28),
#         }
#         result = self.rrd.get_dates()
#         unordered_result = dict(result)
#         assert_equal(unordered_result, expected)
