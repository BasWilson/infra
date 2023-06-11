import sys

from dotenv import load_dotenv
from infra_cli.cli.apply.main import CliApplyMain
from infra_cli.cli.auth.main import CliAuthMain
from infra_cli.cli.destroy.main import CliDestroyMain
from infra_cli.cli.init.main import CliInitMain
from infra_cli.cli.provider.main import CliProviderMain
from infra_cli.cli.reset.main import CliResetMain
from infra_cli.helpers.paths import SetupPaths
from infra_cli.helpers.logs import SetupLogging

# load env from the directory that infra is being called from
SetupPaths()
SetupLogging()
load_dotenv("./.env")

args = sys.argv[1:]


def command():
    # get command from args
    if len(args) == 0:
        print("No command specified")
        print("Usage: infra <command>")
        print("Available commands: init, apply, destroy, provider, reset, auth")
        return

    command = args[0]
    if command == "reset":
        CliResetMain()
    elif command == "init":
        CliInitMain()
    elif command == "apply":
        CliApplyMain()
    elif command == "destroy":
        CliDestroyMain()
    elif command == "provider":
        CliProviderMain()
    elif command == "auth":
        CliAuthMain()
    else:
        print("Command not found")
        print("Usage: infra <command>")
        print("Available commands: init, apply, destroy, provider, reset, auth")
