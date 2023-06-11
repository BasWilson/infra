import os


def ValidateEnvVars(variables):
    for variable in variables:
        if variable not in os.environ:
            raise Exception(f"Missing environment variable: {variable}")
