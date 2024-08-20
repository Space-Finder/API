from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

other_router = APIRouter(
    tags=[
        "Other",
    ],
)


@other_router.get("/")
async def redirect_to_docs() -> RedirectResponse:
    """
    This simply just redirects anyone going to the base url to the swagger api docs
    """

    return RedirectResponse("/docs")


@other_router.get("/ping")
async def ping(request: Request) -> dict:
    """
    Just returns "pong" to the requester
    Useful to check if the api is online
    """

    return {"success": True, "detail": "pong"}
