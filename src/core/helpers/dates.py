from datetime import date, datetime, time

import pytz
from prisma.models import Period
from prisma.enums import Year

from core import prisma


def get_week(d: date | None = None):
    if d is None:
        auckland = pytz.timezone("Pacific/Auckland")
        d = datetime.now(auckland)
    return d.isocalendar()[1]


def is_time_within_period(time_to_check: datetime, period: Period) -> bool:
    start_time_parts = list(map(int, period.startTime.split(":")))
    end_time_parts = list(map(int, period.endTime.split(":")))

    start = time(hour=start_time_parts[0], minute=start_time_parts[1])
    end = time(hour=end_time_parts[0], minute=end_time_parts[1])

    return start <= time_to_check.time() <= end


async def get_period_for_time(date: datetime, year_group: Year) -> Period | None:
    day_of_week = date.weekday()  # Monday is 0, Sunday is 6

    # Timetable is only Mon to Fri (0 to 4)
    if day_of_week > 4:
        return None

    timetable = await get_timetable(year_group, date)
    periods_for_day = timetable[day_of_week]

    for period in periods_for_day:
        if is_time_within_period(date, period):
            return period

    # no match
    return None


async def get_timetable(year_group: Year, date: datetime) -> tuple[
    list[Period],
    list[Period],
    list[Period],
    list[Period],
    list[Period],
]:
    week_number = get_week(date)
    current_year = date.year

    week = await prisma.week.find_first(
        where={"year": current_year, "number": week_number, "yearGroup": year_group},
        include={
            "weekTimetable": {
                "include": {
                    "monday": {
                        "include": {
                            "periods": True,
                        },
                    },
                    "tuesday": {
                        "include": {
                            "periods": True,
                        },
                    },
                    "wednesday": {
                        "include": {
                            "periods": True,
                        },
                    },
                    "thursday": {
                        "include": {
                            "periods": True,
                        },
                    },
                    "friday": {
                        "include": {
                            "periods": True,
                        },
                    },
                }
            }
        },
    )

    if not week or not week.weekTimetable:
        return [[] * 5]  # type: ignore

    timetable = week.weekTimetable

    return [
        timetable.monday.periods,  # type: ignore
        timetable.tuesday.periods,  # type: ignore
        timetable.wednesday.periods,  # type: ignore
        timetable.thursday.periods,  # type: ignore
        timetable.friday.periods,  # type: ignore
    ]
