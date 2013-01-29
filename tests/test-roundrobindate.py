# -*- coding: utf8 -*-

# nosetests --with-coverage --cover-package=roundrobindate ./tests

from nose.tools import *
from roundrobindate import RoundRobinDate
from datetime import datetime, date, timedelta

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

    def test_string_representation(self):
        "Test the class string representation via the magic method __str__"
        expected = "Hello World"
        result = self.rrd.__str__()
        assert_equal(result, expected)

    def test__get_next_month(self):
        expected = 2
        result = self.rrd._get_next_month(1)
        assert_equal(result, expected)

        expected = 1
        result = self.rrd._get_next_month(12)
        assert_equal(result, expected)

    def test__get_previous_month(self):
        expected = 12
        result = self.rrd._get_previous_month(1)
        assert_equal(result, expected)

        expected = 1
        result = self.rrd._get_previous_month(2)
        assert_equal(result, expected)

    def test_set_current_date(self):
        self.rrd.set_current_date(2010,01,05)
        result = self.rrd._get_current_date()
        assert_equal(result.day, 5)
        assert_equal(result.month, 1)
        assert_equal(result.year, 2010)

    def test__get_days_in_month(self):
        result = self.rrd._get_days_in_month(1, 2010)
        assert_equal(result, 31)

        result = self.rrd._get_days_in_month(4, 2010)
        assert_equal(result, 30)

        result = self.rrd._get_days_in_month(2, 2010)
        assert_equal(result, 28)

        result = self.rrd._get_days_in_month(2, 2012)
        assert_equal(result, 29)

        try:
            result = self.rrd._get_days_in_month("4", "2010")
            assert False
        except TypeError:
            assert True

    def test_default_options(self):
        "Test the default options"
        expected = self.rrd._get_default_options()
        result = self.rrd.get_options()
        assert_equal(result, expected)

    # def test_set_option(self):
    #     "Test setting a basic option"

    # def test_set_empty_option(self):
    #     "Test setting a option to empty values"
    #     expected = {}
    #     options = self.rrd.get_options()
    #     assert_equal(result, expected)

    # def test_set_complex_option(self):
    #     "Test setting a option to collections"
    #     expected = {}
    #     options = self.rrd.get_options()
    #     assert_equal(result, expected)
