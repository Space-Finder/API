from datetime import date, datetime

from .period import PERIODS


def get_week(d: date | None = None):
    if d is None:
        d = datetime.now()
    return d.isocalendar()[1]


def get_period_for_time(date: datetime):
    day = date.weekday()
    if day < 0 or day > 4:
        return None  # No periods on Saturday and Sunday

    time_in_minutes = (
        date.hour * 60 + date.minute
    )  # Convert current time to minutes since midnight

    periods = PERIODS[day]
    for period in periods:
        start_hour, start_minute = map(int, period["start"].split(":"))
        end_hour, end_minute = map(int, period["end"].split(":"))

        start_time = start_hour * 60 + start_minute
        end_time = end_hour * 60 + end_minute

        if start_time <= time_in_minutes < end_time:
            return period

    return None
