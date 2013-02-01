# -*- coding: utf8 -*-

# nosetests --with-coverage --cover-package=roundrobindate ./tests

from nose.tools import *
from roundrobindate import RoundRobinDate
from datetime import date, timedelta

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

    def test_get_dates_as_strings_with_retain_days_options(self):
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

    def test_get_dates_with_retain_weeks_options(self):
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

    def test_get_dates_with_retain_weeks_options_with_same_anchor_and_current_dates(self):
        """
        The current day is excluded from week count. It is included in return
        values only because the current day is always returned.
        """
        new_options = {
            "current_date": "2011-01-02",
            "anchor_date": "2011-01-02",
            "days_to_retain": 0,
            "weeks_to_retain": 2,
            "months_to_retain": 0,
            "years_to_retain": 0
        }
        self.rrd.set_options(new_options)

        expected = {
            "2011-01-02": date(2011, 1, 2),
            "2010-12-26": date(2010, 12, 26),
            "2010-12-19": date(2010, 12, 19),
        }
        result = self.rrd.get_dates()
        assert_equal(result, expected)

    def test_get_dates_with_retain_months_options(self):
        new_options = {
            "current_date": "2012-02-02",
            "anchor_date": "2004-02-29",
            "days_to_retain": 0,
            "weeks_to_retain": 0,
            "months_to_retain": 6,
            "years_to_retain": 0
        }
        self.rrd.set_options(new_options)

        expected = {
            "2012-02-02": date(2012, 2, 2),
            "2012-01-28": date(2012, 1, 28),
            "2011-12-28": date(2011, 12, 28),
            "2011-11-28": date(2011, 11, 28),
            "2011-10-28": date(2011, 10, 28),
            "2011-09-28": date(2011, 9, 28),
            "2011-08-28": date(2011, 8, 28)
        }
        result = self.rrd.get_dates()
        assert_equal(result, expected)

    def test_get_dates_with_retain_years_options(self):
        new_options = {
            "current_date": "2012-02-01",
            "anchor_date": "2008-02-29",
            "days_to_retain": 0,
            "weeks_to_retain": 0,
            "months_to_retain": 0,
            "years_to_retain": 5
        }
        self.rrd.set_options(new_options)

        expected = {
            "2012-02-01": date(2012, 2, 1),
            "2011-02-28": date(2011, 2, 28),
            "2010-02-28": date(2010, 2, 28),
            "2009-02-28": date(2009, 2, 28),
            "2008-02-28": date(2008, 2, 28),
            "2007-02-28": date(2007, 2, 28),
        }
        result = self.rrd.get_dates()
        assert_equal(result, expected)

    def test_get_dates_as_strings_with_day_and_week_retain_options(self):
        "Test overlapping dates collapse"
        new_options = {
            "current_date": "2012-02-29",
            "anchor_date": "2012-02-29",
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
            "2012-02-21",
            "2012-02-20"
        ]
        result = self.rrd.get_dates_as_strings()
        assert_equal(result, expected)

    def test_get_dates_as_strings_with_week_and_month_retain_options(self):
        "Illustrate week and month boundaries do not necessarily overlap"
        new_options = {
            "current_date": "2012-01-01",
            "anchor_date": "2012-01-01",
            "days_to_retain": 0,
            "weeks_to_retain": 5,
            "months_to_retain": 1,
            "years_to_retain": 0
        }
        self.rrd.set_options(new_options)

        expected = [
            "2012-01-01",
            "2011-12-25",
            "2011-12-18",
            "2011-12-11",
            "2011-12-04",
            "2011-12-01",
            "2011-11-27",
        ]
        result = self.rrd.get_dates_as_strings()
        assert_equal(result, expected)

    def test_get_dates_with_all_options_with_collapsed_results(self):
        "Show how dates can collapse in. Dates are inward looking."
        new_options = {
            "current_date": "2012-02-29",
            "anchor_date": "2012-02-29",
            "days_to_retain": 1,
            "weeks_to_retain": 1,
            "months_to_retain": 1,
            "years_to_retain": 1
        }
        self.rrd.set_options(new_options)

        expected = {
            "2012-02-29": date(2012, 2, 29),
            "2012-02-28": date(2012, 2, 28),
            "2012-02-22": date(2012, 2, 22),
        }
        result = self.rrd.get_dates()
        assert_equal(result, expected)

    def test_get_dates_with_default_options(self):
        options = {
            "current_date": "2012-02-29",
        }
        self.rrd.set_options(options)

        expected = [
            '2012-02-29',
            '2012-02-28',
            '2012-02-27',
            '2012-02-26',
            '2012-02-25',
            '2012-02-24',
            '2012-02-23',
            '2012-02-19',
            '2012-02-12',
            '2012-02-01',
            '2012-01-01',
            '2011-12-01',
            '2011-11-01',
            '2011-10-01',
            '2011-09-01',
            '2011-01-01',
            '2010-01-01',
            '2009-01-01',
            '2008-01-01',
            '2007-01-01',
            '2006-01-01',
            '2005-01-01',
            '2004-01-01',
            '2003-01-01'
        ]
        result = self.rrd.get_dates_as_strings()
        assert_equal(result, expected)

    def test_get_dates_daily_checks_for_a_month(self):
        """
        Test a full month's worth of daily backups.
        Simulate a repository of past days by using set intersection.
        This simulates the perminant removal of data and checks there
        are no data "gaps" where data is deleted prematurely and can
        not be recovered.
        """
        debug = False
        starting_options = {
            "anchor_date": "2012-05-01",
            "days_to_retain": 1,
            "weeks_to_retain": 4,
            "months_to_retain": 1,
            "years_to_retain": 1
        }
        self.rrd.set_options(starting_options)
        
        for i in xrange(1, 32):
            current_date = "2012-05-{0:02d}".format(i)
            daily_options = {"current_date": current_date}
            self.rrd.set_options(daily_options)
            daily_result = self.rrd.get_dates_as_strings()
            try:
                results_set = results_set.intersection(daily_result)
                today = daily_result.pop(0)
                results_set.add(today)
            except NameError:
                results_set = set(daily_result)
            if debug:
                results_list = list(results_set)
                results_list.sort(reverse=True)
                print(results_list)

        expected = set([
            '2012-05-31',
            '2012-05-30',
            '2012-05-29',
            '2012-05-22',
            '2012-05-15',
            '2012-05-08',
            '2012-05-01',
        ])
        assert_equal(results_set, expected)

    def test_get_dates_daily_checks_for_over_a_year(self):
        """
        Test over a full year's worth of daily backups.
        Simulate a repository of past days by using set intersection.
        This simulates the perminant removal of data and checks there
        are no data "gaps" where data is deleted prematurely and can
        not be recovered.
        """
        debug = False
        starting_options = {
            "anchor_date": "2011-05-23",
            "days_to_retain": 6,
            "weeks_to_retain": 5,
            "months_to_retain": 6,
            "years_to_retain": 2
        }
        self.rrd.set_options(starting_options)
        
        for i in xrange(0, 375):
            current_date = date(2011, 5, 23) + timedelta(days=i)
            daily_options = {"current_date": current_date}
            self.rrd.set_options(daily_options)
            daily_result = self.rrd.get_dates_as_strings()
            try:
                results_set = results_set.intersection(daily_result)
                today = daily_result.pop(0)
                results_set.add(today)
            except NameError:
                results_set = set(daily_result)
            if debug:
                results_list = list(results_set)
                results_list.sort(reverse=True)
                print(results_list)

        expected = set([
            '2011-05-23', # Years to Retain 1
            '2011-12-23', # Months to Retain 1
            '2012-01-23', # Months to Retain 2
            '2012-02-23', # Months to Retain 3
            '2012-03-23', # Months to Retain 4
            '2012-04-23', # Weeks to Retain 1 + Months to Retain 5
            '2012-04-30', # Weeks to Retain 2
            '2012-05-07', # Weeks to Retain 3
            '2012-05-14', # Weeks to Retain 4
            '2012-05-21', # Weeks to Retain 5
            '2012-05-23', # Months to Retain 6 + Years to Retain 2
            '2012-05-25', # Days to Retain 1
            '2012-05-26', # Days to Retain 2
            '2012-05-27', # Days to Retain 3
            '2012-05-28', # Days to Retain 4
            '2012-05-29', # Days to Retain 5
            '2012-05-30', # Days to Retain 6
            '2012-05-31', # Final Day
        ])
        assert_equal(results_set, expected)
