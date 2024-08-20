__all__ = ("image_router",)

from fastapi import APIRouter

image_router = APIRouter(
    tags=[
        "Image",
    ],
    prefix="/api/image",
)
