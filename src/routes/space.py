__all__ = ("space_router",)

from fastapi import APIRouter, Request

from core import prisma

space_router = APIRouter(
    tags=[
        "Spaces",
    ],
    prefix="/api/spaces",
)
