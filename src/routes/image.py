__all__ = ("image_router",)

from io import BytesIO
from os.path import join, dirname
from datetime import datetime, timedelta

import pytz
from prisma.enums import Year
from prisma.models import Booking
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, FileResponse

from core import prisma
from core.helpers.dates import get_week, get_period_for_time
from core.helpers.genimage import generate_common_image

image_router = APIRouter(
    tags=[
        "Image",
    ],
    prefix="/api/image",
)

AUCKLAND = pytz.timezone("Pacific/Auckland")
EMPTY_IMAGE = join(dirname(__file__), "../../", "assets/", "images/empty.png")


@image_router.get("/")
async def generate_image(
    request: Request, common_id: str, time: datetime | None = None, exact: bool = False
):
    empty_response = (
        None
        if request.app.settings.DEVMODE
        else FileResponse(path=EMPTY_IMAGE, media_type="image/png")
    )

    common = await prisma.common.find_unique(where={"id": common_id})
    if common is None:
        return empty_response

    time = datetime.now(AUCKLAND) if time is None else time.astimezone(AUCKLAND)
    if not exact:
        # the timetable will show 5 min before each period
        # so it needs to be access the next period 5 minutes before
        time += timedelta(minutes=5)

    current_year = time.year

    week_number = get_week(time)

    bookings: list[Booking] = []
    for year in [Year.Y11, Year.Y12, Year.Y13]:
        week = await prisma.week.find_first(
            where={"number": week_number, "year": current_year, "yearGroup": year}
        )
        if not week:
            continue

        period = await get_period_for_time(time, year)
        if period is None or period.periodType != "CLASS" or not period.periodNumber:
            continue

        year_bookings = await prisma.booking.find_many(
            where={"periodNumber": period.periodNumber, "weekId": week.id},
            include={
                "course": {"include": {"common": True}},
                "space": {"include": {"common": True}},
                "teacher": {"include": {"user": True}},
            },
        )

        filtered_bookings = [
            booking
            for booking in year_bookings
            if (
                booking.course
                and booking.course.commonId == common_id
                and booking.course.line == period.line
                and booking.course.year == year
            )
        ]

        bookings.extend(filtered_bookings)

    if not bookings:
        return empty_response

    image = generate_common_image(
        common.name, common.primaryColor, common.secondaryColor, bookings
    )

    image_buffer = BytesIO()
    image.save(image_buffer, "PNG")
    image_buffer.seek(0)

    return StreamingResponse(image_buffer, media_type="image/png")
