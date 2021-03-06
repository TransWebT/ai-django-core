import datetime
from calendar import monthrange

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.utils import timezone


class DateHelper:
    # Constants to use for django ORMs `__weekday` lookup to avoid usage of integers directly.
    # Unfortunately python's calendar weekdays are not equivalent to the database ones.
    ORM_SUNDAY = 1
    ORM_MONDAY = 2
    ORM_TUESDAY = 3
    ORM_WEDNESDAY = 4
    ORM_THURSDAY = 5
    ORM_FRIDAY = 6
    ORM_SATURDAY = 7


def get_start_and_end_date_from_calendar_week(year, calendar_week):
    """
    Returns the first and last day of a given calendar week
    :param year: int
    :param calendar_week: int
    :return:
    """
    monday = datetime.datetime.strptime(f'{year}-{calendar_week}-1', "%Y-%W-%w").date()
    return monday, monday + datetime.timedelta(days=6.9)


def get_next_calendar_week(compare_date):
    """
    Returns the next calendar week as an integer
    :param compare_date: date
    :return:
    """
    day_in_one_week = compare_date + datetime.timedelta(days=(7 - compare_date.weekday()))
    return day_in_one_week.isocalendar()[1]


def next_weekday(d, weekday):
    """
    Returns the next date of the given weekday
    For example: next_weekday(d, calendar.MONDAY) would return the next monday starting at date "d"
    :param d: date
    :param weekday: int
    :return:
    """
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


def date_month_delta(start_date: datetime.date, end_date: datetime.date):
    """
    Calculates the number of months lying between two dates.
    So from April 15th to May 1st it's 0.5 months.
    Attention: `end_date` will be excluded in the result (outer border)
    :return: float or False (if `start_date` > `end_date`)
    """

    # If `start_date` is greater, this logic doesn't make any sense
    if start_date > end_date:
        raise NotImplementedError('Start date > end date')

    # Calculate date difference between dates
    date_diff = (end_date - start_date).days

    # Iteration variable
    delta = 0
    iter_date = start_date
    # Loop until all days are processed
    while date_diff > 0:
        # Get days of month we are currently looking at
        iter_month, iter_month_days = monthrange(iter_date.year, iter_date.month)
        # Calculate how many days are left to end of this month
        days_to_month_end = min((iter_month_days - (iter_date.day - 1)), date_diff)
        # Add percentage of the month these days cover to return variable
        delta += days_to_month_end / iter_month_days
        # Reduce leftover days by the amount we already processed
        date_diff -= days_to_month_end

        # Set iteration date to first of next month
        iter_date += relativedelta(months=1, day=1)

    # Return data
    return delta


def tz_today(str_format=None):
    """
    Returns either a timezone-aware today object or string. Depending if the `str_format` param is set.
    :param str_format: If set, formats the date object to a string. Pass strftime-compatible value
    :return:
    """
    if settings.USE_TZ:
        date = timezone.now().date()
    else:
        date = datetime.datetime.now().date()

    if str_format:
        return date.strftime(str_format)
    return date
