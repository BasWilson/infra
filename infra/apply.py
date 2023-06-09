import yaml
from infra.helpers.config import LoadInfraFile
from infra.helpers.constants import ErrorMessages, InfoMessages
from dotenv import load_dotenv

from infra.helpers.logs import PrintError, PrintInfo, SetupLogging
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

    upToDate = resourceState != None and resourceState["resource"] == resource
    outOfDate = resourceState != None and resourceState["resource"] != resource
    doesNotExistYet = resourceState == None

    # check if the resource is already in the desired state
    if  upToDate:
        PrintInfo(InfoMessages["already_in_state"].format(resource["id"]))
        continue


    if outOfDate or doesNotExistYet:
        # apply the resource
        result =  providers[providerName].Apply(resource, createdResources)
        result["resource"] = resource
        createdResources.append(result)

    # Destroy the old resource
    if outOfDate:
        # Note, this state is the old state, not the new state. hence why we can pass it to destroy
        providers[providerName].Destroy(resource, state[resource["id"]])

    PrintInfo(InfoMessages["applied_changes"].format(resource["id"]))

    # update the state
    state = GetState()
    state[resource["id"]] = result
    StoreState(state)