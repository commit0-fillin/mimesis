"""Provider of data related to date and time."""
import typing as t
from calendar import monthrange
from datetime import date, datetime, time, timedelta
from mimesis.compat import pytz
from mimesis.datasets import GMT_OFFSETS, ROMAN_NUMS, TIMEZONES
from mimesis.enums import DurationUnit, TimestampFormat, TimezoneRegion
from mimesis.providers.base import BaseDataProvider
from mimesis.types import Date, DateTime, Time
__all__ = ['Datetime']

class Datetime(BaseDataProvider):
    """Class for generating data related to the date and time."""
    _CURRENT_YEAR = datetime.now().year

    class Meta:
        name = 'datetime'
        datafile = f'{name}.json'

    @staticmethod
    def bulk_create_datetimes(date_start: DateTime, date_end: DateTime, **kwargs: t.Any) -> list[DateTime]:
        """Bulk create datetime objects.

        This method creates a list of datetime objects from
        ``date_start`` to ``date_end``.

        You can use the following keyword arguments:

        * ``days``
        * ``hours``
        * ``minutes``
        * ``seconds``
        * ``microseconds``

        .. warning::

            Empty ``**kwargs`` produces **timedelta(0)** which obviously
            cannot be used as step, so you have to pass valid ``**kwargs``
            for :py:class:`datetime.timedelta` which will be used as a step
            by which ``date_start`` will be incremented until it reaches ``date_end``
            to avoid infinite loop which eventually leads to ``OverflowError``.

        See :py:class:`datetime.timedelta` for more details.

        :param date_start: Begin of the range.
        :param date_end: End of the range.
        :param kwargs: Keyword arguments for :py:class:`datetime.timedelta`
        :return: List of datetime objects
        :raises: ValueError: When ``date_start``/``date_end`` not passed,
            when ``date_start`` larger than ``date_end`` or when the given
            keywords for `datetime.timedelta` represent a non-positive timedelta.
        """
        if not date_start or not date_end:
            raise ValueError("Both date_start and date_end must be provided.")
        if date_start > date_end:
            raise ValueError("date_start must be earlier than date_end.")
        
        step = timedelta(**kwargs)
        if step <= timedelta(0):
            raise ValueError("The timedelta step must be positive.")
        
        result = []
        current = date_start
        while current <= date_end:
            result.append(current)
            current += step
        
        return result

    def week_date(self, start: int=2017, end: int=_CURRENT_YEAR) -> str:
        """Generates week number with year.

        :param start: Starting year.
        :param end: Ending year.
        :return: Week number.
        """
        year = self.random.randint(start, end)
        week = self.random.randint(1, 52)
        return f"{year}-W{week:02d}"

    def day_of_week(self, abbr: bool=False) -> str:
        """Generates a random day of the week.

        :param abbr: Abbreviated day name.
        :return: Day of the week.
        """
        days = self._extract(['day', 'name' if not abbr else 'abbr'])
        return self.random.choice(days)

    def month(self, abbr: bool=False) -> str:
        """Generates a random month of the year.

        :param abbr: Abbreviated month name.
        :return: Month name.
        """
        months = self._extract(['month', 'name' if not abbr else 'abbr'])
        return self.random.choice(months)

    def year(self, minimum: int=1990, maximum: int=_CURRENT_YEAR) -> int:
        """Generates a random year.

        :param minimum: Minimum value.
        :param maximum: Maximum value.
        :return: Year.
        """
        return self.random.randint(minimum, maximum)

    def century(self) -> str:
        """Generates a random century.

        :return: Century.
        """
        centuries = self._extract(['century'])
        return self.random.choice(centuries)

    def periodicity(self) -> str:
        """Generates a random periodicity string.

        :return: Periodicity.
        """
        periodicity = self._extract(['periodicity'])
        return self.random.choice(periodicity)

    def date(self, start: int=2000, end: int=_CURRENT_YEAR) -> Date:
        """Generates a random date object.

        :param start: Minimum value of year.
        :param end: Maximum value of year.
        :return: Formatted date.
        """
        year = self.year(start, end)
        month = self.random.randint(1, 12)
        day = self.random.randint(1, 28)  # Using 28 to avoid invalid dates
        return date(year, month, day)

    def formatted_date(self, fmt: str='', **kwargs: t.Any) -> str:
        """Generates random date as string.

        :param fmt: The format of date, if None then use standard
            accepted in the current locale.
        :param kwargs: Keyword arguments for :meth:`~.date()`
        :return: Formatted date.
        """
        date_obj = self.date(**kwargs)
        if not fmt:
            fmt = self._extract(['formats', 'date'])
        return date_obj.strftime(fmt)

    def time(self) -> Time:
        """Generates a random time object.

        :return: ``datetime.time`` object.
        """
        return time(
            self.random.randint(0, 23),
            self.random.randint(0, 59),
            self.random.randint(0, 59),
            self.random.randint(0, 999999)
        )

    def formatted_time(self, fmt: str='') -> str:
        """Generates formatted time as string.

        :param fmt: The format of time, if None then use standard
            accepted in the current locale.
        :return: String formatted time.
        """
        time_obj = self.time()
        if not fmt:
            fmt = self._extract(['formats', 'time'])
        return time_obj.strftime(fmt)

    def day_of_month(self) -> int:
        """Generates a random day of the month, from 1 to 31.

        :return: Random value from 1 to 31.
        """
        return self.random.randint(1, 31)

    def timezone(self, region: TimezoneRegion | None=None) -> str:
        """Generates a random timezone.

        :param region: Timezone region.
        :return: Timezone.
        """
        if region:
            region = self.validate_enum(region, TimezoneRegion)
            timezones = TIMEZONES[region.value]
        else:
            timezones = [tz for sublist in TIMEZONES.values() for tz in sublist]
        return self.random.choice(timezones)

    def gmt_offset(self) -> str:
        """Generates a random GMT offset value.

        :return: GMT Offset.
        """
        return self.random.choice(GMT_OFFSETS)

    def datetime(self, start: int=_CURRENT_YEAR, end: int=_CURRENT_YEAR, timezone: str | None=None) -> DateTime:
        """Generates random datetime.

        :param start: Minimum value of year.
        :param end: Maximum value of year.
        :param timezone: Set custom timezone (pytz required).
        :return: Datetime
        """
        date_obj = self.date(start, end)
        time_obj = self.time()
        dt = datetime.combine(date_obj, time_obj)
        
        if timezone:
            try:
                tz = pytz.timezone(timezone)
                dt = tz.localize(dt)
            except pytz.exceptions.UnknownTimeZoneError:
                raise ValueError(f"Unknown timezone: {timezone}")
        
        return dt

    def formatted_datetime(self, fmt: str='', **kwargs: t.Any) -> str:
        """Generates datetime string in human-readable format.

        :param fmt: Custom format (default is format for current locale)
        :param kwargs: Keyword arguments for :meth:`~.datetime()`
        :return: Formatted datetime string.
        """
        dt = self.datetime(**kwargs)
        if not fmt:
            fmt = self._extract(['formats', 'datetime'])
        return dt.strftime(fmt)

    def timestamp(self, fmt: TimestampFormat=TimestampFormat.POSIX, **kwargs: t.Any) -> str | int:
        """Generates a random timestamp in given format.

        Supported formats are:

        - TimestampFormat.POSIX
        - TimestampFormat.RFC_3339
        - TimestampFormat.ISO_8601

        Example:

        >>> from mimesis import Datetime
        >>> from mimesis.enums import TimestampFormat
        >>> dt = Datetime()
        >>> dt.timestamp(fmt=TimestampFormat.POSIX)
        1697322442
        >>> dt.timestamp(fmt=TimestampFormat.RFC_3339)
        '2023-12-08T18:46:34'
        >>> dt.timestamp(fmt=TimestampFormat.ISO_8601)
        '2009-05-30T21:45:57.328600'

        :param fmt: Format of timestamp (Default is TimestampFormat.POSIX).
        :param kwargs: Kwargs for :meth:`~.datetime()`.
        :return: Timestamp.
        """
        dt = self.datetime(**kwargs)
        fmt = self.validate_enum(fmt, TimestampFormat)
        
        if fmt == TimestampFormat.POSIX:
            return int(dt.timestamp())
        elif fmt == TimestampFormat.RFC_3339:
            return dt.strftime('%Y-%m-%dT%H:%M:%S')
        elif fmt == TimestampFormat.ISO_8601:
            return dt.isoformat()

    def duration(self, min_duration: int=1, max_duration: int=10, duration_unit: DurationUnit | None=DurationUnit.MINUTES) -> timedelta:
        """Generate a random duration.

        The default duration unit is Duration.MINUTES.

        When the duration unit is None, then random
        duration from DurationUnit is chosen.

        A timedelta object represents a duration, the difference
        between two datetime or date instances.

        :param min_duration: Minimum duration.
        :param max_duration: Maximum duration.
        :param duration_unit: Duration unit.
        :return: Duration as timedelta.
        """
        if duration_unit is None:
            duration_unit = self.random.choice(list(DurationUnit))
        else:
            duration_unit = self.validate_enum(duration_unit, DurationUnit)
        
        value = self.random.randint(min_duration, max_duration)
        
        if duration_unit == DurationUnit.DAYS:
            return timedelta(days=value)
        elif duration_unit == DurationUnit.HOURS:
            return timedelta(hours=value)
        elif duration_unit == DurationUnit.MINUTES:
            return timedelta(minutes=value)
        elif duration_unit == DurationUnit.SECONDS:
            return timedelta(seconds=value)
        elif duration_unit == DurationUnit.MILLISECONDS:
            return timedelta(milliseconds=value)
        elif duration_unit == DurationUnit.MICROSECONDS:
            return timedelta(microseconds=value)
