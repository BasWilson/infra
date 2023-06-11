import sys
from infra_cli.cli.auth.login import CliAuthLogin


def CliAuthMain():
    args = sys.argv[1:]
    if args == None or len(args) < 2:
        print("Usage: infra auth <command>")
        exit(1)

    command = args[1]

    if command == "login":
        remainingArgs = args[2:]
        if len(remainingArgs) < 2:
            print("Usage: infra auth login <username> <password>")
            exit(1)

        username = remainingArgs[0]
        password = remainingArgs[1]

        CliAuthLogin(username, password)
