import os
import requests


def CliProviderList():
    url = os.getenv("BACKEND_URL") if os.getenv("BACKEND_URL") != None else "https://infra-backend-abuah.ondigitalocean.app"
    result = requests.get("{}/providers/".format(url))
    if result.status_code != 200:
        print("Cannot reach backend, are you sure it is running and the BACKEND_URL is correct?")
        exit(1)

    if len(result.json()) == 0:
        print("No providers found")
        exit(0)

    print("Providers:")
    for provider in result.json():
        print(provider["name"]+":")
        # print each wheel
        for wheel in provider["wheels"]:
            print("  {}".format(wheel))