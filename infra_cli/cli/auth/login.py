import os
import requests

from infra_cli.helpers.credentials import SetupCredentials
from requests.auth import HTTPBasicAuth


def CliAuthLogin(username, password):
    url = (
        os.getenv("BACKEND_URL")
        if os.getenv("BACKEND_URL") != None
        else "https://infra-backend-abuah.ondigitalocean.app"
    )
    result = requests.get(
        "{}/users/login".format(url), auth=HTTPBasicAuth(username, password)
    )

    if result.status_code != 200:
        print("Invalid username or password")
        exit(1)

    SetupCredentials(username, password)

    print("Logged in as {}".format(username))
