import boto3
from rich import box
from rich.align import Align
from rich.panel import Panel
from rich.pretty import Pretty
from rich.table import Table
from textual.widget import Widget


class BucketListPanel(Widget):
    def render(self):
        body = Table("Name", box=None, expand=True, show_header=False)

        s3 = boto3.client("s3")
        for bucket in s3.list_buckets()["Buckets"]:
            body.add_row(bucket["Name"])

        return Panel(body, title="Telescope", border_style="blue", box=box.ROUNDED)
