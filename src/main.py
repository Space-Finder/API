""" (script)
python script to start the rest api and load routes
"""

__version__ = "0.0.1"
__author__ = ["FusionSid"]
__licence__ = "MIT License"

import os
from typing import Final
from os.path import dirname, join, exists

import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

from core.helpers.exceptions import InvalidDevmodeValue

load_dotenv()

app = FastAPI()

PORT: Final = 8443 if (port := os.getenv("PORT")) is None else int(port)
SSL_CERTFILE_PATH: Final = join(dirname(__file__), "cert.pem")
SSL_KEYFILE_PATH: Final = join(dirname(__file__), "key.pem")

# check that both certificate files exist
both_certfiles_exist = all([exists(SSL_CERTFILE_PATH), exists(SSL_KEYFILE_PATH)])

# check if to startup api in dev mode or not
devmode = os.environ.get("DEVMODE", "").lower()
if devmode not in ["true", "false"]:
    raise InvalidDevmodeValue(provided=devmode)

# set the uvicorn server options based one dev mode or not
options = (
    {"app": "main:app", "port": PORT, "reload": True}
    if devmode == "true" or not both_certfiles_exist
    else {
        "app": "main:app",
        "reload": False,
        "port": PORT,
        "access_log": False,
        "ssl_keyfile": SSL_KEYFILE_PATH,
        "ssl_certfile": SSL_CERTFILE_PATH,
    }
)


if __name__ == "__main__":
    uvicorn.run(**options)
