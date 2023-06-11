from infra_cli.helpers.paths import GetInfraPath


def IsInLockFile(wheel):
    base = GetInfraPath()
    with open("{}/lock".format(base), "r") as f:
        for line in f.readlines():
            if line.strip() == wheel:
                return True
    return False


def AddToLockFile(wheel):
    if not IsInLockFile(wheel):
        base = GetInfraPath()
        with open("{}/lock".format(base), "a") as f:
            f.write("{}\n".format(wheel))
