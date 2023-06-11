import yaml
from infra_cli.cli.provider.install import CliProviderInstall
from infra_cli.helpers.constants import ErrorMessages, InfoMessages
from infra_cli.helpers.lock_file import IsInLockFile
from infra_cli.helpers.logs import PrintError, PrintInfo


def CheckIfProviderInstalled(provider):
    installed = IsInLockFile(provider)
    if not installed:
        PrintInfo(InfoMessages["provider_not_installed"].format(provider))
        CliProviderInstall(provider)


def LoadProviderConfigByName(provider):
    config = None
    try:
        # check if it is installed
        installed = IsInLockFile(provider)

        if not installed:
            # try to load user created provider first from their infra folder
            with open("infra/providers/{}/config.yaml".format(provider), "r") as stream:
                config = yaml.safe_load(stream)
            PrintInfo(InfoMessages["loaded_user_provider"].format(provider))
    except:
        # was not installed, tried to load user created provider, but failed. try to install it
        # install the provider
        PrintInfo("Attempting to install provider: {}".format(provider))
        CliProviderInstall(provider)

    return config


def LoadInfraFile():
    infra = None
    loadedProviders = {}

    try:
        with open("infra.yaml", "r") as stream:
            infra = yaml.safe_load(stream)
    except:
        PrintError(ErrorMessages["no_infra_file"])
        exit(1)

    # check for resources
    if (
        "resources" not in infra
        or not isinstance(infra["resources"], list)
        or len(infra["resources"]) == 0
    ):
        PrintError(ErrorMessages["no_resources"])
        exit(1)

    resources = infra["resources"]

    resourcesWithoutProvider = [
        resource for resource in resources if "provider" not in resource
    ]
    duplicateResourceIds = [
        resource["id"] for resource in resources if resources.count(resource) > 1
    ]

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
        # config = LoadProviderConfigByName(provider)

        # validate the config
        # check if properties exist
        # if (
        #     config == None
        #     or "name" not in config
        #     or "entrypoint" not in config
        #     or "version" not in config
        # ):
        #     PrintError(
        #         ErrorMessages["provider_config_validation_failed"].format(
        #             provider, provider
        #         )
        #     )
        #     exit(1)

        CheckIfProviderInstalled(provider)

        # read the provider methods
        try:
            loc = {}
            print("import {}.main as provider_{}".format(provider, provider))
            exec(
                "import {}.main as provider_{}".format(  # import providerName.main as providerName_digitalocean
                    provider, provider
                ),
                globals(),
                loc,
            )
            loadedProviders[provider] = loc["provider_{}".format(provider)]
            PrintInfo(InfoMessages["imported_provider"].format(loc))
        except Exception as e:
            print(e)
            PrintError(ErrorMessages["no_provider_class"].format(provider, provider))
            exit(1)

    return {"resources": resources, "providers": loadedProviders}
