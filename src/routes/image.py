from fastapi import APIRouter

image_router = APIRouter(
    tags=[
        "Image",
    ],
    prefix="/api/image",
)
