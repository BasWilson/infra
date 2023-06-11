import sys
from infra_cli.cli.provider.build import CliProviderBuild
from infra_cli.cli.provider.install import CliProviderInstall
from infra_cli.cli.provider.list import CliProviderList
from infra_cli.cli.provider.publish import CliProviderPublish


def CliProviderMain():
    args = sys.argv[1:]
    if args == None or len(args) < 2:
        print("Usage: infra provider <command>")
        exit(1)

    command = args[1]

    if command == "build":
        CliProviderBuild()

    elif command == "publish":
        CliProviderPublish()

    elif command == "install":
        if len(args) < 3:
            print("Usage: infra provider install <provider> <wheel?>")
            exit(1)

        provider = args[2]
        wheel = args[3] if len(args) > 3 else None

        CliProviderInstall(provider, wheel)

    elif command == "new":
        # create new provider
        print("Not implemented yet")

    elif command == "list":
        CliProviderList()
