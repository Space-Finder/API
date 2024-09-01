__all__ = ("booking_router",)

from fastapi import APIRouter, Request

from core import prisma, get_week

booking_router = APIRouter(
    tags=[
        "Bookings",
    ],
    prefix="/api/bookings",
)


@booking_router.get("/")
async def get_bookings(request: Request, teacher_id: str):
    next_week = get_week() + 1

    return await prisma.booking.find_many(
        where={"week": next_week, "teacherId": teacher_id},
    )
