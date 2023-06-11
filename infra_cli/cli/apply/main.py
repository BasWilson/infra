from infra_cli.helpers.config import LoadInfraFile
from infra_cli.helpers.constants import InfoMessages

from infra_cli.helpers.logs import PrintInfo
from infra_cli.helpers.state import GetState, StoreState


def CliApplyMain():
    infra = LoadInfraFile()
    resources = infra["resources"]
    providers = infra["providers"]

    for resource in resources:
        providerName = resource["provider"]
        # get the saved state of the resource
        state = GetState()
        resourceState = state.get(resource["id"], None)

        upToDate = resourceState != None and resourceState["resource"] == resource
        outOfDate = resourceState != None and resourceState["resource"] != resource
        doesNotExistYet = resourceState == None

        # check if the resource is already in the desired state
        if upToDate:
            PrintInfo(InfoMessages["already_in_state"].format(resource["id"]))
            continue

        if outOfDate or doesNotExistYet:
            # apply the resource
            result = providers[providerName].Apply(resource)
            result["resource"] = resource

        # Destroy the old resource
        if outOfDate:
            # Note, this state is the old state, not the new state. hence why we can pass it to destroy
            providers[providerName].Destroy(resource, state[resource["id"]])

        PrintInfo(InfoMessages["applied_changes"].format(resource["id"]))

        # update the state
        state = GetState()
        state[resource["id"]] = result
        StoreState(state)
