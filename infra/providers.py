import os
import sys

import requests
from infra.helpers.paths import SetupPaths
import urllib.request
from dotenv import load_dotenv

load_dotenv()
SetupPaths()

# make request to backend
result = requests.get("{}/providers/".format(os.getenv("BACKEND_URL")))
if result.status_code != 200:
    print("Cannot reach backend, are you sure it is running and the BACKEND_URL is correct?")
    exit(1)

# Print providers

if len(result.json()) == 0:
    print("No providers found")
    exit(0)

print("Providers:")
print("Name | Version")
for provider in result.json():
    print(provider["name"] + " | v" + str(provider["version"]))