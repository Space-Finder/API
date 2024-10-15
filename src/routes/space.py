from fastapi import APIRouter

space_router = APIRouter(
    tags=[
        "Spaces",
    ],
    prefix="/api/spaces",
)
