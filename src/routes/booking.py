from fastapi import APIRouter

booking_router = APIRouter(
    tags=[
        "Bookings",
    ],
    prefix="/api/bookings",
)
