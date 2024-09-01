from datetime import date, datetime

import pytz


def get_week(d: date | None = None):
    if d is None:
        d = datetime.now(pytz.timezone("Pacific/Auckland"))
    return d.isocalendar()[1]


def test():
    dates: list[tuple[date, int]] = [
        (date(2024, 3, 14), 11),
        (date(2024, 8, 29), 35),
        (date(2024, 8, 26), 35),
        (date(2024, 9, 2), 36),
        (date(2024, 12, 5), 49),
    ]
    for [d, w] in dates:
        assert (get_week(d)) == w
