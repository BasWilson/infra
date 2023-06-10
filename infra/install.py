import os
import sys

import requests
from infra.helpers.paths import SetupPaths
import urllib.request
from dotenv import load_dotenv

load_dotenv()
SetupPaths()

# Installs a provider based on command line arguments

args = sys.argv
if len(args) < 3:
    print("Usage: install.py <provider> <version>")
    exit(1)

provider = args[1]
version = args[2]

# check if provider exists
if os.path.exists("providers/" + provider):
    print("Provider already exists, skipping installation")
    exit(1)

# make request to backend
result = requests.get("{}/providers/{}".format(os.getenv("BACKEND_URL"), provider))
if result.status_code != 200:
    print("Provider not found on backend, skipping installation")
    exit(1)

# check if version exists
if version not in result.json()["versions"]:
    print("Version not found, skipping installation")
    exit(1)

print("Installing provider " + provider + " version " + version)

# download provider
urllib.request.urlretrieve(result.json()["baseUrl"] + "/" + version + ".zip", ".infra/downloads/" + version + ".zip")

# unzip provider
os.system("unzip .infra/downloads/" + version + ".zip -d infra/providers/" + provider)

# remove zip file
os.system("rm .infra/downloads/" + version + ".zip")

print("Installation complete for provider " + provider + " version " + version + "")