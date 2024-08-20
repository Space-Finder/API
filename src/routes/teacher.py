__all__ = ("teacher_router",)

import validators
from fastapi import APIRouter, Request

teacher_router = APIRouter(
    tags=[
        "Teacher",
    ],
    prefix="/api/teachers",
)

SCHOOL_DOMAIN = "ormiston.school.nz"
TEACHERS = ["st22209@ormiston.school.nz", "hprasad@ormiston.school.nz"]


@teacher_router.get("/verify")
async def verify_is_teacher(request: Request, email: str):
    # Will be updated to use database, once data is given from Mr Lambert
    conditions = [
        email,
        validators.email(email),
        email.endswith(SCHOOL_DOMAIN),
        email in TEACHERS,
    ]

    return all(conditions)
