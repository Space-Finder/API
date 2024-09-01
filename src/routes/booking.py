__all__ = ("booking_router",)

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from core import prisma, get_week

booking_router = APIRouter(
    tags=[
        "Bookings",
    ],
    prefix="/api/bookings",
)


class Booking(BaseModel):
    week: int
    period: int
    space_id: str
    class_id: str
    teacher_id: str


@booking_router.get("/")
async def get_bookings(request: Request, teacher_id: str):
    next_week = get_week() + 1

    return await prisma.booking.find_many(
        where={"week": next_week, "teacherId": teacher_id},
    )


@booking_router.get("/todo")
async def get_bookings_todo(request: Request, teacher_id: str):
    next_week = get_week() + 1

    classes = await prisma.course.find_many(where={"teacherId": teacher_id})
    if not classes:
        return []

    # Get all bookings for these classes in the next week
    class_ids = [course.id for course in classes]
    bookings = await prisma.booking.find_many(
        where={
            "courseId": {"in": class_ids},
            "teacherId": teacher_id,
            "week": next_week,
        }
    )

    booked_periods = {(booking.courseId, booking.periodNumber) for booking in bookings}

    todo = []
    for course in classes:
        todo.extend(
            {
                "period_number": period,
                "line": course.line,
                "course_id": course.id,
                "common_id": course.commonId,
            }
            for period in [1, 2, 3]
            # Generate the todo list by checking missing periods
            if (course.id, period) not in booked_periods
        )

    return todo


@booking_router.post("/")
async def make_booking(request: Request, booking_data: Booking):
    existing_booking = await prisma.booking.find_first(
        where={
            "week": booking_data.week,
            "periodNumber": booking_data.period,
            "spaceId": booking_data.space_id,
        }
    )

    if existing_booking:
        raise HTTPException(
            status_code=409,
            detail="Booking conflict: This space is already booked for the specified period.",
        )

    new_booking = await prisma.booking.create(
        data={
            "week": booking_data.week,
            "periodNumber": booking_data.period,
            "spaceId": booking_data.space_id,
            "courseId": booking_data.class_id,
            "teacherId": booking_data.teacher_id,
        }
    )

    return {"message": "Booking created successfully", "booking": new_booking}
