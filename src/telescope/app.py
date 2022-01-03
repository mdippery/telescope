from textual.app import App
from textual.widgets import Placeholder


class Telescope(App):
    async def on_load(self, event):
        await self.bind("q", "quit")

    async def on_mount(self, event):
        await self.view.dock(Placeholder(name="main"))
