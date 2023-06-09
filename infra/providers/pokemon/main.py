import random
import requests

from infra.helpers.logs import PrintError


def Apply(resource):
    pokemonName = ""

    try:
        randomId = random.randint(resource.get("minId", 1), resource.get("maxId", 151))
        result = requests.get("https://pokeapi.co/api/v2/pokemon/{}".format(randomId))
        pokemonName = result.json()["name"]

    except Exception as e:
        PrintError(e)
        exit(1)

    return {"pokemonName": pokemonName}


def Destroy(resource, state):
    return None
