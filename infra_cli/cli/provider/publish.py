import os
import requests
import yaml

from infra_cli.helpers.credentials import GetCredentials


def CliProviderPublish():
    url = (
        os.getenv("BACKEND_URL")
        if os.getenv("BACKEND_URL") != None
        else "https://infra-backend-abuah.ondigitalocean.app"
    )
    credentials = GetCredentials()
    if credentials == None:
        print("Not logged in, please run infra auth login")
        exit(1)

    config = None
    try:
        with open("infra-config.yaml", "r") as stream:
            config = yaml.safe_load(stream)
    except:
        print("No infra-config.yaml found, please run infra provider init")
        exit(1)

    # get latest wheel from dist folder
    if not os.path.exists("dist"):
        print("No dist folder found, please run infra provider build")
        exit(1)

    distContents = os.listdir("dist")
    if len(distContents) == 0:
        print("No wheel found in dist folder, please run infra provider build")
        exit(1)

    wheelFiles = [file for file in distContents if file.endswith(".whl")]
    latestWheel = sorted(wheelFiles)[-1]

    pathToWheel = "dist/{}".format(latestWheel)

    # create form data request to upload wheel
    files = {"file": open(pathToWheel, "rb")}

    print("Uploading wheel to infra-backend")
    result = requests.post(
        "{}/providers/{}/{}".format(url, config["name"], latestWheel),
        files=files,
        auth=credentials,
    )

    # upload built wheel to infra-backend
    # requirements: infra provider build, infra auth login
    if result.status_code != 200:
        print(result.json())
        print(
            "Error uploading wheel to infra-backend, are you sure you have the correct permissions?"
        )
        exit(1)

    print("Uploaded {}' wheel to infra-backend".format(config["name"]))
