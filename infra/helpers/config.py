import yaml
from infra.helpers.constants import ErrorMessages, InfoMessages
from infra.helpers.logs import PrintError, PrintInfo

loadedProviders = {}

def LoadInfraFile():
    infra = None

    try:
        with open("infra.yaml", 'r') as stream:
            infra = yaml.safe_load(stream)
    except:
        PrintError(ErrorMessages["no_infra_file"])
        exit(1)

    resources = infra["resources"]
    resourcesWithoutProvider = [resource for resource in resources if "provider" not in resource]
    duplicateResourceIds = [resource["id"] for resource in resources if resources.count(resource) > 1]

    # Validate resources
    if len(resourcesWithoutProvider) > 0:
        PrintError(ErrorMessages["no_provider"].format(resourcesWithoutProvider))
        exit(1)

    if len(duplicateResourceIds) > 0:
        PrintError(ErrorMessages["duplicate_resource_id"].format(duplicateResourceIds))
        exit(1)

    # Get providers
    providers = list(set([resource["provider"] for resource in resources]))

    # Import providers
    for provider in providers:
        # read the config
        config = None
        try:
            with open("iaas/providers/{}/config.yaml".format(provider), 'r') as stream:
                config = yaml.safe_load(stream)
        except:
            PrintError(ErrorMessages["no_config"].format(provider, provider))
            exit(1)

        # validate the config
        # check if properties exist
        if "name" not in config or "entrypoint" not in config or "version" not in config:
            PrintError(ErrorMessages["provider_config_validation_failed"].format(provider, provider))
            exit(1)

        # read the provider methods
        try:
            loc = {}
            exec("import iaas.providers.{}.{} as provider_{}".format(provider, config["entrypoint"], provider), globals(), loc)
            loadedProviders[provider] = loc["provider_{}".format(provider)]
            PrintInfo(InfoMessages["imported_provider"].format(loc))
        except:
            PrintError(ErrorMessages["no_provider_class"].format(provider, provider))
            exit(1)

    return {
        "resources": resources,
        "providers": loadedProviders
    }