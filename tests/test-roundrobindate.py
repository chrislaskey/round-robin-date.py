# -*- coding: utf8 -*-

from nose.tools import *
from roundrobindate import RoundRobinDate

class TestRoundRobinDate():

    def setup(self):
        "Set up test fixtures"
        self.rrd = RoundRobinDate()

    def teardown(self):
        "Tear down test fixtures"

    def test_string_representation(self):
        "Test the class string representation via the magic method __str__"
        expected = "Hello World"
        result = self.rrd.__str__()
        assert_equal(result, expected)

    # def test_default_options(self):
    #     "Test the default options"
    #     expected = {}
    #     result = self.rrd.get_options()
    #     assert_equal(result, expected)

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
