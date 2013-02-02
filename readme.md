About
================================================================================

Version 1.0.1

A python library for calculating round-robin database style dates.

 	# Assuming current date is 2013-02-01 ./python
	>>> From roundrobindate import RoundRobinDate options = {"days_to_retain":
	>>> 1, "weeks_to_retain": 1, "months_to_retain": 1, "years_to_retain": 2}
	>>> RoundRobinDate(options).get_dates_as_strings()
	['2013-02-01', '2013-01-31', '2013-01-28', '2013-01-01', '2012-01-01']	

The goal is to provide a stable set of _inclusive_ backup intervals based on
flexible date options. 

To illustrate what is meant by inclusive intervals, take a month backup for
example. Month backups are always run on the same day of the month. They will
never be > 31 days older than the current date, but they may be younger than 31
days. In other words, assuming the ```backup_day_of_month``` is 5 and the
current day is 2/20/2012, the first month backup will be on 2/5/2012 and the
second month backup is on 1/5/2012.

This empowers the library user to choose exactly the backup plan required, with
no assumptions and unwanted extra backups. It does mean users should think
carefully before setting the ```*_to_retain``` options very carefully.

When in doubt test output using the ```current_date``` option. For more
examples see the unit tests, there are a few included for illustration,
including some trickier edge-cases.

Quickstart
----------

There are a lot of edge cases to the way the calendar system works, and it can
be tricky to anticipate them all. This tool provides a stable set of
_inclusive_ backup intervals, meaning a 364 day old backup may be retained as
the 1 year backup date, but a 367 day will not. So when in doubt set n+1 for
all ```*_to_retain``` options from what may be expected.

Documentation
=============

Methods
-------

```set_options()``` (dict, {option_name: option_value}) New values will always
trump old values. See Options section for available options and acceptable
values.

```get_options()``` () Returns a dictionary where each key is the option name,
and each value the current option value.

```get_dates()``` () Returns a dictionary where each key is an ISO 8601 format
compatible string, 'YYYY-MM-DD', and the value is a datetime.date object.

```get_dates_as_strings()``` () Returns a list of dates in a ISO 8601 format
compatible string, 'YYYY-MM-DD'.

Options
-------

All options are set using Python dictionaries, ```{option_name:
option_value}```. Options can be passed to a RoundRobinDate object either in
the constructor call as the first argument or after object initiation using the
```set_options()``` method. Values can be set as one mutli-key dictionary or
one at a time using single-key dictionaries.

```current_date``` (datetime.date | string, "YYYY-MM-DD") By default this is
set to the current value using datetime.date.today(). It can be set to any
valid date value within datetime.MAXYEAR and datetime.MINYEAR. Can pass either
a datetime.date or a ISO 8601 format compatible string, 'YYYY-MM-DD'.

```days_to_retain``` (int) How many previous days to include, excluding the
current day.

```weeks_to_retain``` (int) How many weeks to include prior to the current
date, excluding the current day. This is always the same day of the week, which
is set by the ```backup_day_of_week``` option or derived from
a ```anchor_date``` option value.

```months_to_retain``` (int) How many months to include prior to the current
date, excluding the current day. This is always the same day of the month,
which is set by the ```backup_day_of_month``` option or derived from
a ```anchor_date``` option value.

```years_to_retain``` (int) How many years to include prior to the current
date, excluding the current day. This is always the same day of the week, which
is set by the ```backup_month_of_year``` option or derived from
a ```anchor_date``` option value.

```backup_day_of_week``` (int, 1-7 for Monday-Sunday) By default this is set to
1.

```backup_day_of_month``` (int, 1-31*) By default this is set to 1. *If a 
value > 28 requires ```auto_correct_backup_dates``` to be set to True, otherwise
will raise an error.

```backup_month_of_year``` (int, 1-12) By default this is set to 1.

```anchor_date``` (datetime.date | "YYYY-MM-DD") By default this is not set.
Instead of setting individual ```backup_*_of_*``` options, a single date can be
input and each of these values auto generated. Useful in automatic backup
scripts where the ific initial backup date does not have to be specified.

```auto_correct_backup_dates``` (True | False) By default this is set to True.
To ensure stable backup dates ```backup_day_of_month``` values can not be > 28.
The ```auto_correct_backup_dates``` option will automatically adjust ```backup
_*_of_*``` values to the 1st of the following month. This allows backups to
start immediately if the current date is > 28, while maintaining stable backup
intervals. Also useful in automatic backup scripts where the initial backup
date is dynamic and may fall on a day of the month > 28, allowing immediate
backups without human intervention.

Use cases
=========

Implementing a backup system
----------------------------

The most common application of a round robin date library is to implement
a backup system. A simple way to implement such a system is to use the first
backup day as the ```anchor_date```. During each backup keep the oldest date,
the current date, and the returned round robin dates. Discard the other dates.
For a working example see the ```tests/test-roundrobindate.py``` file, the last
tests are integration style tests to confirm a simple backup system can be run
without unexpected data loss. Remember to test assumptions about option values
before releasing anything out the wild.

License
================================================================================

All code is released under MIT license. See the attached LICENSE.txt file for
more information, including commentary on license choice.
