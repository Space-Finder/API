""" (script)
python script to start the rest api and load routes
"""

__version__ = "0.0.1"
__author__ = ["Siddhesh Zantye"]
__licence__ = "MIT License"


from typing import Final
from os.path import dirname, join, exists

import uvicorn
from rich import print
from dotenv import load_dotenv

from core import SpaceFinder
from routes import router_list, middleware_list

SSL_CERTFILE_PATH: Final = join(dirname(__file__), "cert.pem")
SSL_KEYFILE_PATH: Final = join(dirname(__file__), "key.pem")

load_dotenv()
app = SpaceFinder(__version__)

# iterate through routers list and include them all
for route in router_list:
    app.include_router(router=route)

# iterate through middleware list and include them all
for middleware in middleware_list:
    app.add_middleware(middleware)


def main() -> None:
    # check that both certificate files exist
    both_certfiles_exist = all([exists(SSL_CERTFILE_PATH), exists(SSL_KEYFILE_PATH)])
    run_in_devmode = app.settings.DEVMODE or not both_certfiles_exist

    BASE_OPTIONS = {
        "app": "main:app",
        "port": app.settings.PORT,
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
