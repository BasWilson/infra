import os
from requests.auth import HTTPBasicAuth
from infra_cli.helpers.paths import GetInfraPath


def SetupCredentials(username, password):
    base = GetInfraPath()
    credentialsPath = "{}/credentials".format(base)
    if os.path.exists(credentialsPath):
        os.remove(credentialsPath)

    with open(credentialsPath, "x") as f:
        f.write("{}\n{}".format(username, password))


def GetCredentials():
    # read credentials file
    base = GetInfraPath()
    credentialsPath = "{}/credentials".format(base)
    if not os.path.exists(credentialsPath):
        return None

    with open(credentialsPath, "r") as f:
        lines = f.readlines()
        if len(lines) < 2:
            return None

        username = lines[0].strip()
        password = lines[1].strip()

        return HTTPBasicAuth(username, password)
