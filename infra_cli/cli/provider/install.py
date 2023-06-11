import os
import requests
from infra_cli.helpers.lock_file import AddToLockFile, IsInLockFile

from infra_cli.helpers.paths import GetInfraPath
import urllib.request


def CliProviderInstall(provider, wheel=None):
    base = GetInfraPath()
    url = (
        os.getenv("BACKEND_URL")
        if os.getenv("BACKEND_URL") != None
        else "https://infra-backend-abuah.ondigitalocean.app"
    )

    if provider == None:
        print("Usage: infra provider install <provider> <wheel?>")
        exit(1)

    print("Looking for provider {}, wheel {}".format(provider, wheel))

    # make request to backend
    result = requests.get("{}/providers/{}".format(url, provider))
    if result.status_code != 200 or "wheels" not in result.json():
        print("Provider not found on backend, skipping installation")
        exit(1)

    # check if wheel exists
    if wheel != None and wheel not in result.json()["wheels"]:
        print("Wheel not found, skipping installation")
        exit(1)

    # assign wheel
    if wheel == None:
        wheel = result.json()["wheels"][0]

    if not IsInLockFile(wheel):
        print("Installing provider {}, wheel {}".format(provider, wheel))

        # prepare dir
        os.makedirs("{}/providers/{}".format(base, provider), exist_ok=True)

        # download provider
        urllib.request.urlretrieve(
            "{}/{}".format(result.json()["baseUrl"], wheel),
            "{}/providers/{}/{}".format(base, provider, wheel),
        )

        #  install wheel
        os.system(
            "pip3 install {}/providers/{}/{} --force-reinstall > /dev/null".format(
                base, provider, wheel
            )
        )

        # mark as installed in lock file
        AddToLockFile(wheel)

        print("Installation complete for provider {}, wheel {}".format(provider, wheel))
