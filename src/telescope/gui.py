import math

import boto3
from rich import box
from rich.align import Align
from rich.panel import Panel
from rich.pretty import Pretty
from rich.table import Table
from textual.reactive import Reactive
from textual.widget import Widget


class BucketListPanel(Widget):
    page = Reactive(1)

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
    def max_items_per_page(self):
        return self.console.size[1] - 2

    @property
    def first_item(self):
        return self.max_items_per_page * (self.page - 1)

    @property
    def last_item(self):
        return self.max_items_per_page * self.page

    @property
    def min_page(self):
        return 1

    @property
    def max_page(self):
        return math.ceil(len(self.buckets) / self.max_items_per_page)

    def render(self):
        body = Table("Name", box=None, expand=True, show_header=False)

        start, end = self.first_item, self.last_item
        for bucket in self.buckets[start:end]:
            body.add_row(bucket["Name"])

        return Panel(body, title="Buckets", border_style="blue", box=box.ROUNDED)

    def page_forward(self):
        # TODO: Don't show blanks at end of last page
        if self.page + 1 <= self.max_page:
            self.page += 1

    def page_back(self):
        if self.page - 1 >= self.min_page:
            self.page -= 1
