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

    def test_get_today(self):
        new_options = {
            "current_date": "2011-01-01",
            "days_to_retain": 0,
            "weeks_to_retain": 0,
            "months_to_retain": 0,
            "years_to_retain": 0
        }
        self.rrd.set_options(new_options)

        expected = "2011-01-01"
        result = self.rrd.get_today()
        assert_equal(result, expected)

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
            "anchor_date": "2004-01-15",
            "days_to_retain": 0,
            "weeks_to_retain": 0,
            "months_to_retain": 6,
            "years_to_retain": 0
        }
        self.rrd.set_options(new_options)

        expected = [
            "2012-02-02", # Today's backup
            "2012-01-15", # Month backup 1
            "2011-12-15", # Month backup 2
            "2011-11-15", # Month backup 3
            "2011-10-15", # Month backup 4
            "2011-09-15", # Month backup 5
            "2011-08-15"  # Month backup 6
        ]
        result = self.rrd.get_dates_as_strings()
        assert_equal(result, expected)

    def test_get_dates_with_retain_years_options(self):
        new_options = {
            "current_date": "2012-02-01",
            "anchor_date": "2008-02-28",
            "days_to_retain": 0,
            "weeks_to_retain": 0,
            "months_to_retain": 0,
            "years_to_retain": 5
        }
        self.rrd.set_options(new_options)

        expected = [
            "2012-02-01", # Today's backup
            "2011-02-28", # Year backup 1
            "2010-02-28", # Year backup 2
            "2009-02-28", # Year backup 3
            "2008-02-28", # Year backup 4
            "2007-02-28"  # Year backup 5
        ]
        result = self.rrd.get_dates_as_strings()
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

    def test_get_dates_with_generic_options(self):
        "Illustrates generic options with no strange edge cases."
        new_options = {
            "current_date": "2010-10-20",
            "anchor_date": "2010-10-20",
            "days_to_retain": 6,
            "weeks_to_retain": 4,
            "months_to_retain": 6,
            "years_to_retain": 2
        }
        self.rrd.set_options(new_options)

        expected = [
            "2010-10-20", # Today's date
            "2010-10-19", # Retain day 1
            "2010-10-18", # Retain day 2
            "2010-10-17", # Retain day 3
            "2010-10-16", # Retain day 4
            "2010-10-15", # Retain day 5
            "2010-10-14", # Retain day 6
            "2010-10-13", # Retain week 1
            "2010-10-06", # Retain week 2
            "2010-09-29", # Retain week 3
            "2010-09-22", # Retain week 4
            "2010-09-20", # Retain month 1
            "2010-08-20", # Retain month 2
            "2010-07-20", # Retain month 3
            "2010-06-20", # Retain month 4
            "2010-05-20", # Retain month 5
            "2010-04-20", # Retain month 6
            "2009-10-20", # Retain year 1
            "2008-10-20", # Retain year 2
        ]
        result = self.rrd.get_dates_as_strings()
        assert_equal(result, expected)

    def test_get_dates_with_all_options_and_illustrate_collapsed_results(self):
        """
        Be aware backup intervals are never longer than their interval.
        Notice how the 1 years_to_retain value switches to a recent value after
        365+1 days.
        """
        new_options = {
            "current_date": "2012-11-15", # 366 days after anchor date
            "anchor_date": "2011-11-14",
            "days_to_retain": 1,
            "weeks_to_retain": 1,
            "months_to_retain": 1,
            "years_to_retain": 1
        }
        self.rrd.set_options(new_options)

        expected = [
            "2012-11-15", # Today's backup
            "2012-11-14", # Year backup 1 && Month backup && Day backup 1
            "2012-11-12", # Weekly backup 1
        ]
        result = self.rrd.get_dates_as_strings()
        assert_equal(result, expected)

    def test_get_dates_with_all_options_and_illustrate_late_in_month_auto_corrected_dates(self):
        """
        When auto correct backup dates is on and a date is given where 
        backup_day_of_month > 28, the 1st day of the next month is used for
        the backup_day_of_month and backup_month_of_year values instead.
        """
        new_options = {
            "current_date": "2012-01-30",
            "anchor_date": "2012-01-30",
            "auto_correct_backup_dates": True,
            "days_to_retain": 1,
            "weeks_to_retain": 1,
            "months_to_retain": 1,
            "years_to_retain": 1
        }
        self.rrd.set_options(new_options)

        expected = [
            "2012-01-30", # Today's backup
            "2012-01-29", # Day backup 1
            "2012-01-23", # Week backup 1
            "2012-01-01", # Month backup 1
            "2011-02-01", # Year backup 1
        ]
        result = self.rrd.get_dates_as_strings()
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
            '2012-02-20',
            '2012-02-13',
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
