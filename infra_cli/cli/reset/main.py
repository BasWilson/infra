import os
import shutil
from infra_cli.helpers.paths import GetInfraPath, SetupPaths


def CliResetMain():
    # create infra.yaml if not exists
    for root, dirs, files in os.walk("{}".format(GetInfraPath())):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

    SetupPaths()
