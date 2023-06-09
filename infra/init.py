import os
from infra.helpers.paths import SetupPaths

SetupPaths()

# create infra.yaml if not exists
if not os.path.exists("infra.yaml"):
    print("Creating infra.yaml")
    with open("infra.yaml", 'w') as stream:
        stream.write("version: 0.0.1\nresources:")
else:
    print("infra.yaml already exists, skipping creation")