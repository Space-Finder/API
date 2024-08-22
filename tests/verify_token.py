from google.oauth2 import id_token
from google.auth.transport import requests

CLIENT_ID = ""
TOKEN = ""


def verify_token(token):
    id_info = id_token.verify_oauth2_token(
        token,
        requests.Request(),
        CLIENT_ID,
    )
    print(id_info)


verify_token(TOKEN)
