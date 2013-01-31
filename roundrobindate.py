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

    def get_dates(self):
        dates = self._generate_dates()
        return dates

    def _generate_dates(self):
        dates = {}
        dates.update(self._generate_todays_date())
        dates.update(self._generate_day_dates())
        dates.update(self._generate_week_dates())
        dates.update(self._generate_month_dates())
        dates.update(self._generate_year_dates())
        return dates

    def _generate_todays_date(self):
        current_date = self.options["current_date"]
        current_date_dict = self._generate_date_dict(current_date)
        return current_date_dict

    def _generate_date_dict(self, input_date):
        date_key = input_date.isoformat()
        date_value = input_date
        date_dict = {date_key: date_value}
        return date_dict

    def _generate_day_dates(self):
        dates = {}
        current_date = self.options["current_date"]
        number_to_generate = self.options.get("days_to_retain")
        for i in xrange(number_to_generate):
            current_date = self._get_previous_day(current_date)
            date_dict = self._generate_date_dict(current_date)
            dates.update(date_dict)
        return dates

    def _get_previous_day(self, input_date):
        interval = timedelta(days=-1)
        previous_day = input_date + interval
        return previous_day

    def _generate_week_dates(self):
        dates = {}
        current_date = self.options["current_date"]
        current_week_date = self._get_first_week(current_date)
        number_to_generate = self.options.get("weeks_to_retain")
        for i in xrange(number_to_generate):
            date_dict = self._generate_date_dict(current_week_date)
            dates.update(date_dict)
            current_week_date = self._get_previous_week(current_week_date)
        return dates

    def _get_first_week(self, input_date):
        """
        Picks a day of the week based on the backup_day_of_week value.
        Excludes the current day.
        """
        days_in_week = 7
        backup_day_of_week = self.options.get("backup_day_of_week")
        current_day_of_week = input_date.isoweekday()
        if current_day_of_week > backup_day_of_week:
            days_back = current_day_of_week - backup_day_of_week
        else:
            days_back = (current_day_of_week + days_in_week) - backup_day_of_week
        first_week = input_date - timedelta(days=days_back)
        return first_week

    def _get_previous_week(self, input_date):
        interval = timedelta(weeks=-1)
        previous_week = input_date + interval
        return previous_week

    def _generate_month_dates(self):
        dates = {}
        current_date = self.options["current_date"]
        number_to_generate = self.options.get("months_to_retain")
        for i in xrange(number_to_generate):
            current_date = self._get_previous_month(current_date)
            date_dict = self._generate_date_dict(current_date)
            dates.update(date_dict)
        return dates

    def _get_first_month(self, input_date):
        assert("FAILURE: Round Robin Class not complete")
        # TODO: finish month and year date generators.
        pass

    def _get_previous_month(self, input_date):
        day = input_date.day
        month = input_date.month
        year = input_date.year
        if month == 1:
            month = 12
            year = year - 1
        else:
            month = month - 1
        if day > 28:
            day = 28
        previous_month = date(year, month, day)
        return previous_month

    def _generate_year_dates(self):
        dates = {}
        current_date = self.options["current_date"]
        number_to_generate = self.options.get("years_to_retain")
        for i in xrange(number_to_generate):
            current_date = self._get_previous_year(current_date)
            date_dict = self._generate_date_dict(current_date)
            dates.update(date_dict)
        return dates

    def _get_previous_year(self, input_date):
        day = input_date.day
        month = input_date.month
        year = input_date.year
        if day == 29 and month == 2:
            day = 28
        year = year - 1
        previous_year = date(year, month, day)
        return previous_year

    def get_dates_as_strings(self):
        dates = self.get_dates()
        dates_list = list(dates)
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
            "current_date": date.today(),
            "anchor_date": None,
            "backup_day_of_week": 0,
            "backup_day_of_month": 1,
            "backup_month_of_year": 1,
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
        self._parse_current_date_options()
        self._parse_backup_options()
        self._parse_retain_options()

    def _parse_current_date_options(self):
        current_date = self.options.get("current_date")
        parsed_current_date = self._parse_date(current_date)
        self.options["current_date"] = parsed_current_date

    def _parse_date(self, input):
        if isinstance(input, date):
            return input
        else:
            parsed_date = self._parse_string_date(input)
            return parsed_date

    def _parse_string_date(self, input):
        if len(input) < 10:
            raise Exception("Invalid string date: must be in ISO 8601 format,\
                            'YYYY-MM-DD'")
        date_pieces = {
            "year": int(input[0:4]),
            "month": int(input[5:7]),
            "day": int(input[8:10])
        }
        parsed_date = date(
            date_pieces.get("year"),
            date_pieces.get("month"),
            date_pieces.get("day"),
        )
        return parsed_date

    def _parse_backup_options(self):
        anchor_date = self.options.get("anchor_date")
        if anchor_date:
            self._parse_anchor_date()
            self._set_backup_day_options_based_on_anchor_date()
        else:
            self._parse_backup_day_options()

    def _parse_anchor_date(self):
        anchor_date = self.options.get("anchor_date")
        parsed_anchor_date = self._parse_date(anchor_date)
        self.options["anchor_date"] = parsed_anchor_date

    def _set_backup_day_options_based_on_anchor_date(self):
        anchor_date = self.options.get("anchor_date")
        day_of_week = anchor_date.isoweekday()
        day_of_month = anchor_date.day
        month_of_year = anchor_date.month
        if day_of_month > 28:
            day_of_month = 28
        self.options["backup_day_of_week"] = day_of_week
        self.options["backup_day_of_month"] = day_of_month
        self.options["backup_month_of_year"] = month_of_year

    def _parse_backup_day_options(self):
        day_of_week = self.options.get("backup_day_of_week")
        day_of_month = self.options.get("backup_day_of_month")
        month_of_year = self.options.get("backup_month_of_year")
        day_of_week = int(day_of_week)
        day_of_month = int(day_of_month)
        if day_of_month > 28:
            day_of_month = 28
        month_of_year = int(month_of_year)
        self.options["backup_day_of_week"] = day_of_week
        self.options["backup_day_of_month"] = day_of_month
        self.options["backup_month_of_year"] = month_of_year

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
