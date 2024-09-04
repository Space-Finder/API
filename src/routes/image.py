__all__ = ("image_router",)

from io import BytesIO
from datetime import datetime, timedelta

import pytz
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Request, HTTPException

from core import prisma, get_week
from core.helpers import get_period_for_time
from core.helpers.genimage import generate_common_image

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
            "teacher": {"include": {"user": True}},
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

    image = generate_common_image(
        common.name, common.color, common.color2, filtered_bookings
    )
    image_buffer = BytesIO()
    image.save(image_buffer, "PNG")
    image_buffer.seek(0)

    return StreamingResponse(image_buffer, media_type="image/png")
