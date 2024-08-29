from datetime import date, datetime


def get_week(d: date | None = None):
    if d is None:
        d = datetime.now()
    return d.isocalendar()[1]
