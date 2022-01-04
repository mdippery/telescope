import boto3
from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty
from rich.table import Table
from textual.widget import Widget


console = Console()


class BucketListPanel(Widget):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self._buckets = None

    @property
    def buckets(self):
        if not self._buckets:
            s3 = boto3.client("s3")
            self._buckets = s3.list_buckets()["Buckets"]
        return self._buckets

    @property
    def max_items(self):
        return console.size[1] - 2

    @property
    def first_item(self):
        return self.max_items * (self.page - 1)

    @property
    def last_item(self):
        return self.max_items * self.page

    def render(self):
        body = Table("Name", box=None, expand=True, show_header=False)

        start, end = self.first_item, self.last_item
        for bucket in self.buckets[start:end]:
            body.add_row(bucket["Name"])

        return Panel(body, title="Buckets", border_style="blue", box=box.ROUNDED)
