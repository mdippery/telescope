from textual.app import App
from textual.keys import Keys

from telescope.gui import BucketListPanel


class Telescope(App):
    async def on_load(self, event):
        await self.bind("q", "quit")
        # TODO: Figure out how to page with space
        await self.bind("f", "page_forward")
        await self.bind(Keys.PageDown, "page_forward")
        await self.bind("b", "page_back")
        await self.bind(Keys.PageUp, "page_back")
        await self.bind("j", "select_next")
        await self.bind(Keys.Down, "select_next")
        await self.bind("k", "select_previous")
        await self.bind(Keys.Up, "select_previous")

    async def on_mount(self, event):
        self.panel = BucketListPanel(1)
        await self.view.dock(self.panel)

    async def action_page_forward(self):
        self.panel.page_forward()

    async def action_page_back(self):
        self.panel.page_back()

    async def action_select_next(self):
        self.panel.select_next()

    async def action_select_previous(self):
        self.panel.select_previous()
