import yaml
from infra.helpers.config import LoadInfraFile
from dotenv import load_dotenv
from infra.helpers.constants import InfoMessages

from infra.helpers.logs import  PrintInfo, SetupLogging
from infra.helpers.paths import SetupPaths
from infra.helpers.state import GetState, StoreState

load_dotenv()
SetupPaths() # Also done in iaas/init.py, but to be sure we do it here as well
SetupLogging()

infra = LoadInfraFile()
resources = infra["resources"]
providers = infra["providers"]

createdResources = []

for resource in resources:
    providerName = resource["provider"]

    # get the saved state of the resource
    state =  GetState()
    resourceState = state.get(resource["id"], None)

    # check if the resource is already in the desired state
    if resourceState == None:
        PrintInfo(InfoMessages["resource_not_created_yet"].format(resource["id"]))
        continue

    # get the destroy method from loaded provider and call it
    providers[providerName].Destroy(resource, resourceState)

    PrintInfo(InfoMessages["destroyed_resource"].format(resource["id"]))

    # update the state
    state = GetState()
    if resource["id"] in state:
        del state[resource["id"]]

    StoreState(state)