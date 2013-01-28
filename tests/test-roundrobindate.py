# -*- coding: utf8 -*-

from nose.tools import *
from roundrobindate import RoundRobinDate

def setup():
    "set up test fixtures"

def teardown():
    "tear down test fixtures"

@with_setup(setup, teardown)
def test_hello_world():
    "throwaway test to establish hello world with application class."
    rrdate = RoundRobinDate()
    result = rrdate.hello_world()
    expected = "Hello World"
    assert_equal(result, expected)
