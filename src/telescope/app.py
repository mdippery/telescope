from textual.app import App

from telescope.gui import BucketListPanel


class Telescope(App):
    async def on_load(self, event):
        await self.bind("q", "quit")
        # TODO: Figure out how to page with space
        await self.bind("f", "page_forward")
        await self.bind("b", "page_back")

    async def on_mount(self, event):
        self.panel = BucketListPanel(1)
        await self.view.dock(self.panel)

    async def action_page_forward(self):
        self.panel.page_forward()

    async def action_page_back(self):
        self.panel.page_back()
