__all__ = ("course_router",)

from fastapi import APIRouter

course_router = APIRouter(
    tags=[
        "Class",
    ],
    prefix="/api/courses",
)
