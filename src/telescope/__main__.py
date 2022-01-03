import os.path

import boto3

from telescope.app import Telescope


def main():
    # TODO: Configure for non-Mac platforms
    log_path = os.path.join("~", "Library", "Logs", "aws-telescope.log")
    log_path = os.path.expanduser(log_path)
    Telescope.run(title="Telescope", log=log_path)
    # s3 = boto3.client("s3")
    # for bucket in s3.list_buckets()["Buckets"]:
    #     print(bucket["Name"])


if __name__ == "__main__":
    main()
