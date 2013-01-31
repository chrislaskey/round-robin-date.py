#!/usr/bin/env python

from datetime import date, timedelta
from collections import OrderedDict

class RoundRobinDate:

    def __init__(self, options=""):
        self.set_options(options)

    def set_options(self, options):
        if not hasattr(self, "options_parser"):
            self.options_parser = RoundRobinDateOptionsParser()
        self.options_parser.set_options(options)
        self.options = self.options_parser.get_options()

    def get_options(self):
        return self.options.copy()

    def _get_current_date(self):
        "Abstracted to a method to allow unit tests to set value of 'today'"
        return date.today()

    def get_dates(self, direction="past"):
        self._parse_direction(direction)
        dates = self._generate_dates()
        return dates

    def _parse_direction(self, direction):
        allowed = ["past", "future"]
        if direction not in allowed:
            raise Exception("Invalid direction value: must be either 'past'\
                            or 'future'")
        self.direction = direction

    def _generate_dates(self):
        dates = OrderedDict()
        dates.update(self._generate_day_dates())
        dates.update(self._generate_week_dates())
        dates.update(self._generate_month_dates())
        dates.update(self._generate_year_dates())
        return dates

    def _generate_day_dates(self):
        dates = {}
        current_date = self.options.get("start_date")
        number_to_generate = self.options.get("days_to_retain")
        if number_to_generate > 0: # Include start_date
            date_dict = self._generate_date_dict(current_date)
            dates.update(date_dict)
            number_to_generate = number_to_generate - 1
        for i in xrange(number_to_generate):
            current_date = self._get_next_day(current_date)
            date_dict = self._generate_date_dict(current_date)
            dates.update(date_dict)
        return dates

    def _generate_date_dict(self, input_date):
        date_key = input_date.isoformat()
        date_value = input_date
        date_dict = {date_key: date_value}
        return date_dict

    def _get_next_day(self, input_date):
        if self._direction_is_past():
            interval = timedelta(days=-1)
        else:
            interval = timedelta(days=1)
        next_day = input_date + interval
        return next_day

    def _direction_is_past(self):
        return self.direction == "past"

    def _generate_week_dates(self):
        dates = {}
        current_date = self.options.get("start_date")
        number_to_generate = self.options.get("weeks_to_retain")
        for i in xrange(number_to_generate):
            current_date = self._get_next_week(current_date)
            date_dict = self._generate_date_dict(current_date)
            dates.update(date_dict)
        return dates

    def _get_next_week(self, input_date):
        if self._direction_is_past():
            interval = timedelta(weeks=-1)
        else:
            interval = timedelta(weeks=1)
        next_week = input_date + interval
        return next_week

    def _generate_month_dates(self):
        dates = {}
        current_date = self.options.get("start_date")
        number_to_generate = self.options.get("months_to_retain")
        for i in xrange(number_to_generate):
            current_date = self._get_next_month(current_date)
            date_dict = self._generate_date_dict(current_date)
            dates.update(date_dict)
        return dates

    def _get_next_month(self, input_date):
        day = input_date.day
        month = input_date.month
        year = input_date.year
        if self._direction_is_past():
            if month == 1:
                month = 12
                year = year - 1
            else:
                month = month - 1
        else:
            if month == 12:
                month = 1
                year = year + 1
            else:
                month = month + 1
        if day > 28:
            day = 28
        next_month = date(year, month, day)
        return next_month

    def _generate_year_dates(self):
        dates = {}
        current_date = self.options.get("start_date")
        number_to_generate = self.options.get("years_to_retain")
        for i in xrange(number_to_generate):
            current_date = self._get_next_year(current_date)
            date_dict = self._generate_date_dict(current_date)
            dates.update(date_dict)
        return dates

    def _get_next_year(self, input_date):
        day = input_date.day
        month = input_date.month
        year = input_date.year
        if day == 29 and month == 2:
            day = 28
        if self._direction_is_past():
            year = year - 1
        else:
            year = year + 1
        next_year = date(year, month, day)
        return next_year

    def get_dates_as_strings(self, direction="past"):
        dates = self.get_dates(direction)
        dates_list = list(dates)
        dates_list.sort()
        if self._direction_is_past():
            dates_list.sort(reverse=True)
        return dates_list

class RoundRobinDateOptionsParser:

    def __init__(self, custom_options=""):
        self.set_default_options()
        self.set_options(custom_options)

    def set_default_options(self):
        self.options = {}
        default_options = self._get_default_options()
        self.set_options(default_options)

    def _get_default_options(self):
        default_options = {
            "start_date": date.today(),
            "days_to_retain": 7,
            "weeks_to_retain": 3,
            "months_to_retain": 6,
            "years_to_retain": 20
        }
        return default_options

    def set_options(self, new_options):
        """
        Update options, with either a complete or partial options dictionary.
        If partial the new options are merged with current options dictionary.
        """
        if new_options:
            self.options.update(new_options)
            self._parse_options()

    def _parse_options(self):
        self._parse_start_date_options()
        self._parse_retain_options()

    def _parse_start_date_options(self):
        start_date = self.options.get("start_date")
        if not start_date:
            raise Exception("Invalid option for 'start_date': cannot be empty")
        if not isinstance(start_date, date):
            parsed_date = self._parse_string_date(start_date)
            self.options["start_date"] = date(
                parsed_date.get("year"),
                parsed_date.get("month"),
                parsed_date.get("day"),
            )

    def _parse_string_date(self, input):
        if len(input) < 10:
            raise Exception("Invalid string date: must be in ISO 8601 format,\
                            'YYYY-MM-DD'")
        date_pieces = {
            "year": int(input[0:4]),
            "month": int(input[5:7]),
            "day": int(input[8:10])
        }
        return date_pieces

    def _parse_retain_options(self):
        options_with_numeric_values = [
            "days_to_retain",
            "weeks_to_retain",
            "months_to_retain",
            "years_to_retain"
        ]
        for key, value in self.options.iteritems():
            if key in options_with_numeric_values:
                self.options[key] = int(value)

    def get_options(self):
        return self.options.copy()
