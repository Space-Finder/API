from datetime import date, datetime

import pytz


def get_week(d: date | None = None):
    if d is None:
        auckland = pytz.timezone("Pacific/Auckland")
        d = datetime.now(auckland)
    return d.isocalendar()[1]
