__all__ = ("teacher_router",)

from fastapi import APIRouter

teacher_router = APIRouter(
    tags=[
        "Teacher",
    ],
    prefix="/api/teachers",
)
