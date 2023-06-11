import os
import requests
import urllib.request


def CliProviderBuild():
    # url = os.getenv("BACKEND_URL") if os.getenv("BACKEND_URL") != None else "https://infra-backend-abuah.ondigitalocean.app"
    # spaces = os.getenv("S3_URL") if os.getenv("S3_URL") != None else "https://infra-providers.ams3.digitaloceanspaces.com"
    # # For now, we will download a copy of the infra package and install it manually as a wheel. but in the future we can just have a published package.
    # result = requests.get("{}/".format(url))
    # if result.status_code != 200:
    #     print("Cannot reach backend, are you sure it is running and the BACKEND_URL is correct?")
    #     exit(1)

    # # check if version exists
    # if "infra-api" not in result.json():
    #     print("Invalid response from Infra backend")
    #     exit(1)

    # version = result.json()["infra-api"]

    # print("Downloading latest infra-cli wheel, version {}".format(version))

    # # download wheel
    # wheel = "infra-{}-py3-none-any.whl".format(version)
    # urllib.request.urlretrieve("{}/cli/{}".format(spaces, wheel), wheel)

    # install all dependencies and build provider's wheel
    os.system("poetry install && poetry build")
