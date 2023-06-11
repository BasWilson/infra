from infra_cli.helpers.config import LoadInfraFile
from infra_cli.helpers.constants import InfoMessages

from infra_cli.helpers.logs import PrintInfo
from infra_cli.helpers.paths import SetupPaths
from infra_cli.helpers.state import GetState, StoreState


def CliDestroyMain():
    infra = LoadInfraFile()
    resources = infra["resources"]
    providers = infra["providers"]

    for resource in resources:
        providerName = resource["provider"]

        # get the saved state of the resource
        state = GetState()
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
