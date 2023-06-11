import os


def SetupPaths():
    base = GetInfraPath()
    if not os.path.exists(base):
        print("Creating infra directory")
        os.makedirs(base)

    lockPath = "{}/lock".format(base)
    if not os.path.exists(lockPath):
        open(lockPath, "w").close()

    logsPath = "{}/logs".format(base)
    if not os.path.exists(logsPath):
        os.makedirs(logsPath)

    statePath = "{}/state".format(base)
    if not os.path.exists(statePath):
        os.makedirs(statePath)

    downloadsPath = "{}/downloads".format(base)
    if not os.path.exists(downloadsPath):
        os.makedirs(downloadsPath)

    providersPath = "{}/providers".format(base)
    if not os.path.exists(providersPath):
        os.makedirs(providersPath)


def GetInfraPath():
    base = os.path.realpath(os.path.dirname(__file__))
    return base + "/../.infra"
