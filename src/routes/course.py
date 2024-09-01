__all__ = ("course_router",)

from fastapi import APIRouter, Request, HTTPException

from core import prisma

course_router = APIRouter(
    tags=[
        "Class",
    ],
    prefix="/api/courses",
)


@course_router.get("/")
async def get_classes(request: Request, teacher_id: str):
    classes = await prisma.course.find_many(
        where={"teacherId": teacher_id},
    )
    if not classes:
        raise HTTPException(status_code=404, detail="No classes found for this teacher")

    return classes
