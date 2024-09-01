__all__ = ("booking_router",)

from fastapi import APIRouter, Request

from core import prisma, get_week

booking_router = APIRouter(
    tags=[
        "Bookings",
    ],
    prefix="/api/bookings",
)
