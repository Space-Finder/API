""" (script)
python script to start the rest api and load routes
"""

__version__ = "0.0.1"
__author__ = ["Siddhesh Zantye"]
__licence__ = "MIT License"

import os
from json import loads
from typing import Final
from os.path import dirname, join, exists
from contextlib import asynccontextmanager

import uvicorn
from rich import print
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import ValidationError

from core import prisma
from core.models.env import Settings
from routes import router_list, middleware_list
from core.helpers.exceptions import InvalidDevmodeValue, NoDatabaseURL

SSL_CERTFILE_PATH: Final = join(dirname(__file__), "cert.pem")
SSL_KEYFILE_PATH: Final = join(dirname(__file__), "key.pem")


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


# needs to be outside main function for uvicorn to work
load_dotenv()
app = FastAPI(lifespan=lifespan)

# iterate through routers list and include them all
for route in router_list:
    app.include_router(router=route)

# iterate through middleware list and include them all
for middleware in middleware_list:
    app.add_middleware(middleware)


def main() -> None:
    try:
        settings = Settings(**{})
    except ValidationError as err:
        error_value = loads(err.json())[0]["loc"][0]

        if error_value == "DEVMODE":
            raise InvalidDevmodeValue(provided=os.environ.get("DEVMODE", "")) from err
        elif error_value == "DATABASE_URL":
            raise NoDatabaseURL() from err

        raise err

    # check that both certificate files exist
    both_certfiles_exist = all([exists(SSL_CERTFILE_PATH), exists(SSL_KEYFILE_PATH)])
    run_in_devmode = settings.DEVMODE or not both_certfiles_exist

    BASE_OPTIONS = {
        "app": "main:app",
        "port": settings.PORT,
    }

    OPTIONS = (
        {
            **BASE_OPTIONS,
            "reload": True,
        }
        if run_in_devmode
        else {
            **BASE_OPTIONS,
            "reload": False,
            "access_log": False,
            "ssl_keyfile": SSL_KEYFILE_PATH,
            "ssl_certfile": SSL_CERTFILE_PATH,
        }
    )
    print(f"[bold blue]Running in dev mode:[/] {run_in_devmode}")
    print("[bold blue]Starting Up Server...")
    uvicorn.run(**OPTIONS)


if __name__ == "__main__":
    main()
