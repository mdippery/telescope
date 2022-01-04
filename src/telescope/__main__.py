import os
import os.path
import platform
import warnings

import boto3

from telescope.app import Telescope


def logdir():
    plat = platform.system().lower()
    if plat == "darwin":
        return os.path.expanduser(os.path.join("~", "Library", "Logs"))
    elif plat == "linux":
        return os.path.join("/", "tmp")
    # TODO: bsd and others
    else:
        return os.getcwd()


def main():
    warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
    log_path = os.path.join(logdir(), "aws-telescope.log")
    Telescope.run(title="Telescope", log=log_path)


if __name__ == "__main__":
    main()
