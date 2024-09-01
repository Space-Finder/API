from datetime import datetime

import pytz
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from core import get_week
from core.helpers import get_period_for_time

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


@other_router.get("/api/week")
async def week_number(request: Request) -> dict:
    """
    returns the week number
    """

    return {"success": True, "week": get_week()}


@other_router.get("/api/current_period")
async def get_period_from_time(request: Request, time: datetime | None = None) -> dict:
    """
    Returns the period thats occuring during the time provided
    (Uses UTC time)
    """

    auckland = pytz.timezone("Pacific/Auckland")
    time = datetime.now(auckland) if time is None else time.astimezone(auckland)

    return {"success": True, "period": get_period_for_time(time)}
