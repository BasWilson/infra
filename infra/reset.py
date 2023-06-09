import glob
import os
import shutil
from infra.helpers.paths import SetupPaths

# create infra.yaml if not exists
for root, dirs, files in os.walk('.infra'):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))

SetupPaths()
