__all__ = ("space_router",)

from fastapi import APIRouter, Request, HTTPException

from core import prisma, get_week

space_router = APIRouter(
    tags=[
        "Spaces",
    ],
    prefix="/api/spaces",
)


@space_router.get("/available")
async def get_available(request: Request, period: int, common_id: str, line: int):
    next_week = get_week() + 1

    # Fetch all spaces in the specified common area
    all_spaces = await prisma.space.find_many(where={"commonId": common_id})

    if not all_spaces:
        raise HTTPException(status_code=404, detail="No spaces found")

    # Get booked spaces for the specified week, period, and common area
    booked_spaces = await prisma.booking.find_many(
        where={
            "week": next_week,
            "periodNumber": period,
        },
        include={"space": True, "course": True},
    )

    # Extract booked space IDs for quick lookup set
    # ALL the speed, my speed, your speed even--
    booked_space_ids = {
        booking.spaceId
        for booking in booked_spaces
        if booking.space
        and booking.course
        and booking.space.commonId == common_id
        and booking.course.line == line
    }

    return [space for space in all_spaces if space.id not in booked_space_ids]
