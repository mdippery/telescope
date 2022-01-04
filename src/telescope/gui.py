import math

import boto3
from rich import box
from rich.align import Align
from rich.panel import Panel
from rich.pretty import Pretty
from rich.table import Table
from rich.text import Text
from textual.reactive import Reactive
from textual.widget import Widget


def StandardPanel(renderable, title):
    return Panel(renderable, title=title, border_style="blue", box=box.ROUNDED)


def StandardTable(*cols):
    return Table(*cols, box=None, expand=True, show_header=False)


class PagePanel(Widget):
    page = Reactive(1)
    cursor = Reactive(0)

    def __init__(self, page):
        super().__init__()
        self.page = page

    @property
    def max_items_per_page(self):
        return self.console.size[1] - 2

    @property
    def first_item(self):
        if self.page == self.max_page:
            return max(len(self.items) - self.max_items_per_page, 0)
        return self.max_items_per_page * (self.page - 1)

    @property
    def last_item(self):
        return min(self.max_items_per_page * self.page, len(self.items)) - 1

    @property
    def min_page(self):
        return 1

    @property
    def max_page(self):
        return math.ceil(len(self.items) / self.max_items_per_page)

    @property
    def min_item(self):
        return 0

    @property
    def max_item(self):
        return len(self.items) - 1

    @property
    def item(self):
        return self.buckets[self.cursor]

    def page_forward(self):
        if self.page + 1 <= self.max_page:
            self.page += 1
            self.cursor = self.first_item
        else:
            self.console.bell()

    def page_back(self):
        if self.page - 1 >= self.min_page:
            self.page -= 1
            self.cursor = self.last_item
        else:
            self.console.bell()

    def select_next(self):
        if self.cursor + 1 <= self.max_item:
            self.cursor += 1
            if self.cursor > self.last_item:
                self.page_forward()
        else:
            self.console.bell()

    def select_previous(self):
        if self.cursor - 1 >= self.min_item:
            self.cursor -= 1
            if self.cursor < self.first_item:
                self.page_back()
        else:
            self.console.bell()


class BucketListPanel(PagePanel):
    def __init__(self, page):
        super().__init__(page)
        self._buckets = None

    @property
    def buckets(self):
        if not self._buckets:
            s3 = boto3.client("s3")
            self._buckets = s3.list_buckets()["Buckets"]
        return self._buckets

    items = buckets

    def render(self):
        body = StandardTable("Name")

        start, end = self.first_item, self.last_item + 1
        for i, bucket in enumerate(self.buckets[start:end], start):
            text = bucket["Name"]
            if i == self.cursor:
                text = Text(text, style="reverse")
            body.add_row(text)

        return StandardPanel(body, title="Buckets")


class BucketExplorerPanel(PagePanel):
    bucket = Reactive('')
    prefix = Reactive('')

    def __init__(self, page):
        super().__init__(page)
        self._files = []

    @property
    def title(self):
        return self.prefix or self.bucket

    @property
    def files(self):
        if self.bucket and not self._files:
            s3 = boto3.client("s3")
            resp = s3.list_objects(Bucket=self.bucket, Prefix=self.prefix)
            try:
                self._files = resp["Contents"]
            except KeyError:
                self._files = []
        return self._files

    items = files

    def render(self):
        body = StandardTable("Name")

        # TODO: Add ../ entry
        # TODO: Display as folder hierarchy
        start, end = self.first_item, self.last_item + 1
        for i, file in enumerate(self.files[start:end], start):
            text = file["Key"]
            if i == self.cursor:
                text = Text(text, style="reverse")
            body.add_row(text)

        return StandardPanel(body, title=self.title)

    def _reset(self):
        self.page = 1
        self.cursor = 0
        self._files = []

    def watch_bucket(self, bucket):
        self._reset()

    def watch_prefix(self, prefix):
        self._reset()


class HelpPanel(Widget):
    def __init__(self, commands):
        super().__init__()
        self.commands = commands

    def render(self):
        body = StandardTable("Keystroke", "Description")
        for cmd in self.commands:
            body.add_row(" / ".join(cmd.keys), cmd.description)
        # TODO: Add version/copyright to help
        return StandardPanel(body, title="Help")
