import os
import platform
import sys
import warnings
from pathlib import Path

import boto3
import botocore.exceptions
from rich import print

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


def verify_credentials():
    sts = boto3.client("sts")
    try:
        _ = sts.get_caller_identity()
    except botocore.exceptions.UnauthorizedSSOTokenError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)


def main():
    warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
    verify_credentials()
    log_path = logdir() / "aws-telescope.log"
    Telescope.run(title="Telescope", log=str(log_path))


if __name__ == "__main__":
    main()
