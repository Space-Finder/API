""" (module) api
This contains the API class (FastAPI subclass)
"""

__all__ = ("SpaceFinder", "limiter")

import os
from json import loads
from typing import Final
from os.path import dirname, join, exists
from contextlib import asynccontextmanager

from rich import print
from pydantic import ValidationError
from slowapi.extension import Limiter
from fastapi.responses import JSONResponse
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request, Response
from slowapi.middleware import SlowAPIMiddleware
from fastapi.middleware.cors import CORSMiddleware

from core.db import prisma
from core.models.env import Settings
from core.helpers.exceptions import (
    NoAssetsDirectory,
    NoDatabaseURL,
    InvalidDevmodeValue,
)

ASSETS_DIRECTORY = join(dirname(__file__), "../../../", "assets/")
try:
    assert exists(ASSETS_DIRECTORY)
except AssertionError as error:
    raise NoAssetsDirectory from error

DEFAULT_GLOBAL_RATELIMIT: Final = "60/minute"
limiter = Limiter(  # exported
    key_func=get_remote_address,
    default_limits=[DEFAULT_GLOBAL_RATELIMIT],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs when api is starting up
    print("[bold green]Server Started Up Successfully![/]")
    print("[bold blue]Connecting To Database...[/]")
    await prisma.connect()
    print("[bold green]Connected To Database Successfuly![/]")

    yield  # the api is just running normally

    # Runs before api has shut down
    print("[bold blue]Disconnecting From Database...[/]")
    await prisma.disconnect()
    print("[bold blue]Shutting Down Server[/]")


def get_description() -> str:
    """
    Get the description for the api that will be displayed in the docs

    Returns:
        str: The api's description
    """

    path = join(ASSETS_DIRECTORY, "markdown/description.md")
    with open(path) as f:
        return f.read()


def rate_limit_exceeded_handler(request: Request, exc) -> Response:
    response = JSONResponse(
        {
            "success": False,
            "detail": f"Rate limit exceeded: {exc.detail}",
            "tip": "Slow down buddy its really not that deep",
        },
        status_code=429,
    )
    response = request.app.state.limiter._inject_headers(
        response, request.state.view_rate_limit
    )
    return response


class SpaceFinder(FastAPI):
    """
    This is a subclass of fastapi.FastAPI
    """

    def __init__(self, version: str, **kwargs) -> None:
        # swagger docs metadata
        super().__init__(
            title="Space Finder REST API",
            version=version,
            description=get_description(),
            license_info={
                "name": "MIT LICENCE",
                "url": "https://opensource.org/licenses/MIT",
            },
            lifespan=lifespan,
            **kwargs,
        )

        try:
            self.settings = Settings(**{})
        except ValidationError as err:
            error_value = loads(err.json())[0]["loc"][0]

            if error_value == "DEVMODE":
                raise InvalidDevmodeValue(
                    provided=os.environ.get("DEVMODE", "")
                ) from err
            elif error_value == "DATABASE_URL":
                raise NoDatabaseURL() from err

            raise err

        # cors support
        cors_options = {
            "allow_origins": ["http://localhost:3000"],
            "allow_methods": ["*"],
            "allow_headers": ["*"],
            "allow_credentials": True,
        }
        self.add_middleware(CORSMiddleware, **cors_options)

        self.state.limiter = limiter
        self.add_middleware(SlowAPIMiddleware)
        self.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
