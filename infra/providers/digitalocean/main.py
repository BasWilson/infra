import os
import requests

from infra.helpers.logs import PrintError

def Apply(resource, createdResources = []):
    count = resource["count"] if "count" in resource else 1
    jsonResponses = []

    for i in range(count):
        id = resource["id"].concat(i) if count > 1 else resource["id"]
        try:
            if resource["type"] == "droplet":
                response = requests.post("https://api.digitalocean.com/v2/droplets", json={
                    "name": id,
                    "region": resource["region"],
                    "size": resource["size"],
                    "image": resource["image"],
                    "ssh_keys": resource.get("ssh_keys", []),
                    "backups": resource.get("backups", False),
                    "ipv6": resource.get("ipv6", False),
                    "monitoring": resource.get("monitoring", True),
                    "user_data": resource.get("user_data", ""),
                }, headers={
                    "Authorization": "Bearer {}".format(os.getenv("DIGITALOCEAN_TOKEN"))
                })
                jsonResponses.append(response.json())

        except Exception as e:
            PrintError(e)
            PrintError("Failed to create digitalocean resource with id {}".format(id))
            exit(1)

    # We will return the json responses. Might be useful for resources created further in the chain
    return {
        "jsonResponses": jsonResponses
    }

def Destroy(resource, state):
    count = resource["count"] if "count" in resource else 1

    for i in range(count):
        id = resource["id"].concat(i) if count > 1 else resource["id"]
        try:
            if resource["type"] == "droplet":
                createJsonRespons = state["jsonResponses"][i]
                idOfCreatedDroplet = createJsonRespons["droplet"]["id"]
                response = requests.delete("https://api.digitalocean.com/v2/droplets/{}".format(idOfCreatedDroplet), headers={
                    "Authorization": "Bearer {}".format(os.getenv("DIGITALOCEAN_TOKEN"))
                })

                if response.status_code != 204:
                    PrintError(response.json())
                    PrintError("Failed to destroy digitalocean resource with id {}".format(id))
                    exit(1)

        except Exception as e:
            PrintError(e)
            PrintError("Failed to destroy digitalocean resource with id {}".format(id))
            exit(1)

    return None;