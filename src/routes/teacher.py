__all__ = ("teacher_router",)

import validators
from fastapi import APIRouter, Request

from core import prisma

teacher_router = APIRouter(
    tags=[
        "Teacher",
    ],
    prefix="/api/teachers",
)

SCHOOL_DOMAIN = "ormiston.school.nz"


@teacher_router.get("/verify")
async def verify_is_teacher(request: Request, email: str):
    teachers_list = {teacher.email for teacher in await prisma.teacher.find_many()}

    conditions = [
        email,
        validators.email(email),
        email.endswith(SCHOOL_DOMAIN),
        email in teachers_list,
    ]

    return {"success": True, "isTeacher": all(conditions)}
