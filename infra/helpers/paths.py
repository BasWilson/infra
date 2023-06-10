import os


def SetupPaths():
    if not os.path.exists(".infra"):
        os.makedirs(".infra")

    if not os.path.exists(".infra/logs"):
        os.makedirs(".infra/logs")

    if not os.path.exists(".infra/state"):
        os.makedirs(".infra/state")

    if not os.path.exists(".infra/downloads"):
        os.makedirs(".infra/downloads")