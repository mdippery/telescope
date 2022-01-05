import os
import platform
import warnings
from pathlib import Path

import boto3

from telescope.app import Telescope


def logdir():
    plat = platform.system().lower()
    if plat == "darwin":
        return Path.home() / "Library" / "Logs"
    elif plat == "linux":
        return Path("/tmp")
    # TODO: bsd and others
    else:
        return Path.cwd()


def main():
    warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
    log_path = logdir() / "aws-telescope.log"
    Telescope.run(title="Telescope", log=str(log_path))


if __name__ == "__main__":
    main()
