__all__ = ("image_router",)

from datetime import datetime, timedelta

import pytz
from fastapi import APIRouter, Request, HTTPException

from core import prisma, get_week
from core.helpers import get_period_for_time

image_router = APIRouter(
    tags=[
        "Image",
    ],
    prefix="/api/image",
)


AUCKLAND = pytz.timezone("Pacific/Auckland")


@image_router.get("/")
async def generate_image(
    request: Request, common_id: str, time: datetime | None = None
):
    common = await prisma.common.find_unique(where={"id": common_id})
    if common is None:
        raise HTTPException(404, "No common exists with this ID")

    time = datetime.now(AUCKLAND) if time is None else time.astimezone(AUCKLAND)
    # the timetable will show 5 min before each period
    # so it needs to be access the next period 5 minutes before
    time += timedelta(minutes=5)

    week = get_week(time)
    period = get_period_for_time(time)

    if period is None or period["type"] != "class":
        return None

    line = period["line"]
    period_number = period["periodNumber"]

    bookings = await prisma.booking.find_many(
        where={"periodNumber": period_number, "week": week},
        include={
            "course": {"include": {"common": True}},
            "space": {"include": {"common": True}},
        },
    )

    filtered_bookings = [
        booking
        for booking in bookings
        if (
            booking.course
            and booking.space
            and booking.course.commonId == common_id
            and booking.course.line == line
        )
    ]

    return filtered_bookings

    # name = common.name
    # primary_color = common.color
    # secondary_color = common.color2
