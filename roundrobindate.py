#!/usr/bin/env python

from datetime import datetime, date, timedelta

class RoundRobinDate:

    def __init__(self, options=""):
        self.options = self._get_default_options()
        # self.set_options(options)

    def __str__(self):
        "Display current options"
        return "Hello World"

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

    def _get_previous_month(self, month):
        # TODO: Depricated
        if month == 1:
            return 12
        else:
            return month - 1

    def _get_current_date(self):
        "Abstracted current date to aid testing by inheritence"
        return date.now()

    # def _parse_datetime(self, options):
    #     pass

    # def generate(self, start_date=""):
    #     pass

        
    def _get_default_options(self):
        default_options = {
            "start_date": date.today(),
            "days_to_retain": 7,
            "weeks_to_retain": 3,
            "months_to_retain": '6',
            "years_to_retain": 20
        }
        return default_options

    # def set_options(self, new_options):
    #     """
    #     Update options, accepts either complete or partial options dictionary.
    #     If partial the new options are merged with current options dictionary.
    #     """
    #     if new_options:
    #         self.options.update(new_options)
    #         self._parse_options()

    # def _parse_options(self):
    #     self._parse_start_date_options()
    #     self._parse_retain_options()

    # def _parse_start_date_options(self):
    #     start_date = self.options.get("start_date")
    #     if not start_date:
    #         raise Exception("Invalid option for 'start_date': cannot be empty")
    #     if not isinstance(start_date, date):
    #         start_date_as_date = date(start_date)
    #         self.options["start_date"] = start_date_as_date

    # def _parse_retain_options(self):
    #     key_prefixes = ["days", "weeks", "months", "years"]
    #     keys = [ x + "_to_retain" for x in key_prefixes ]
    #     updated_values = { key: int(value) for (key, value) in self.options.iteritems() if value in keys }
    #     self.options.update(updated_values)

    def get_options(self):
        return self.options
