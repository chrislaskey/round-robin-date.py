#!/usr/bin/env python

from datetime import date, timedelta

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

    def _get_days_in_month(self, month, year=""):
        "Get days by subtracting a day from the beginning of next month"
        next_month = self._get_next_month(month)
        if not year:
            year = date.today().year
        last_day_of_month = date(year, next_month, 1) - timedelta(days=1)
        return last_day_of_month.day

    def _get_next_month(self, month):
        if month == 12:
            return 1
        else:
            return month + 1

    def _get_current_date(self):
        "Abstracted to a method to allow unit tests to set 'today'"
        return date.today()

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
        if len(input) < 8:
            raise Exception("Invalid string date: must be in YYYYMMDD format")
        date_pieces = {
            "year": int(input[0:4]),
            "month": int(input[4:6]),
            "day": int(input[6:8])
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
