import os.path

import boto3

from telescope.app import Telescope


def main():
    # TODO: Configure for non-Mac platforms
    log_path = os.path.join("~", "Library", "Logs", "aws-telescope.log")
    log_path = os.path.expanduser(log_path)
    Telescope.run(title="Telescope", log=log_path)


if __name__ == "__main__":
    main()
