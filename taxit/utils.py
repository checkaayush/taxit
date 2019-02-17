"""Generic utility functions"""

import calendar
import datetime as dt
from dateutil.rrule import rrule, MONTHLY


def date_ranges(start_date, end_date):
    """
    Returns calendar months date ranges between given months.
    This will always return the list of calendar months between
    the first day of start_date.month and the last day of end_date.month
    """
    start = get_month_day_range(start_date)[0]
    end = get_month_day_range(end_date)[1]
    recurrences = list(rrule(MONTHLY, dtstart=start, until=end))

    out_date_ranges = []
    for recurrence in recurrences:
        out_date_ranges.append(get_month_day_range(recurrence))

    return out_date_ranges


def get_month_day_range(date):
    """
    For a date 'date' returns the start and end date for the month of 'date'.

    Month with 31 days:
    >>> date = dt.date(2011, 7, 27)
    >>> get_month_day_range(date)
    (datetime.date(2011, 7, 1), datetime.date(2011, 7, 31))

    Month with 28 days:
    >>> date = dt.date(2011, 2, 15)
    >>> get_month_day_range(date)
    (datetime.date(2011, 2, 1), datetime.date(2011, 2, 28))
    """
    first_day = date.replace(day=1)
    last_day = date.replace(day=calendar.monthrange(date.year, date.month)[1])
    return (dt.datetime.combine(first_day, dt.datetime.min.time()),
            dt.datetime.combine(last_day, dt.datetime.max.time()))
