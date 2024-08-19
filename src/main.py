""" (script)
python script to start the rest api and load routes
"""

__version__ = "0.0.1"
__author__ = ["Siddhesh Zantye"]
__licence__ = "MIT License"

import os
from typing import Final
from os.path import dirname, join, exists

import uvicorn
from rich import print
from fastapi import FastAPI
from dotenv import load_dotenv

from core.helpers.exceptions import InvalidDevmodeValue

PORT: Final = 8443 if (port := os.getenv("PORT")) is None else int(port)
SSL_CERTFILE_PATH: Final = join(dirname(__file__), "cert.pem")
SSL_KEYFILE_PATH: Final = join(dirname(__file__), "key.pem")

# needs to be outside main function for uvicorn to work
load_dotenv()
app = FastAPI()


def main() -> None:
    # check that both certificate files exist
    both_certfiles_exist = all([exists(SSL_CERTFILE_PATH), exists(SSL_KEYFILE_PATH)])

    # check if to startup api in dev mode or not
    devmode = os.environ.get("DEVMODE", "").lower()
    if devmode not in ["true", "false"]:
        raise InvalidDevmodeValue(provided=devmode)
    run_in_devmode = devmode == "true" or not both_certfiles_exist

    # set the uvicorn server options based one dev mode or not
    options = (
        {
            "app": "main:app",
            "port": PORT,
            "reload": True,
        }
        if run_in_devmode
        else {
            "app": "main:app",
            "reload": False,
            "port": PORT,
            "access_log": False,
            "ssl_keyfile": SSL_KEYFILE_PATH,
            "ssl_certfile": SSL_CERTFILE_PATH,
        }
    )
    print(f"[bold blue]Running in dev mode:[/] {run_in_devmode}")
    print("[bold blue]Starting Up Server")
    uvicorn.run(**options)


if __name__ == "__main__":
    main()
