from dataclasses import dataclass

from textual.app import App
from textual.keys import Keys
from textual.reactive import Reactive

from telescope.gui import BucketExplorerPanel, BucketListPanel, HelpPanel


@dataclass
class Command:
    keys: list[str]
    action: str
    description: str


class Telescope(App):
    COMMANDS = [
        Command(["q"], "quit", "Quit Telescope"),
        Command(
            ["f", Keys.ControlF, Keys.PageDown],
            "page_forward",
            "Show next page",
        ),
        # TODO: Figure out how to page with space
        Command(
            ["b", Keys.ControlB, Keys.PageUp],
            "page_back",
            "Show previous page",
        ),
        Command(
            ["j", Keys.Down],
            "select_next",
            "Select next item",
        ),
        Command(
            ["k", Keys.Up],
            "select_previous",
            "Select previous item",
        ),
        Command(
            [Keys.Enter, "o", Keys.Right],
            "open_selected_item",
            "Open selected item",
        ),
        Command(["?"], "toggle_help", "Show or hide Telescope help"),
    ]

    show_help = Reactive(False)
    show_explorer = Reactive(False)

    async def on_load(self, event):
        for cmd in Telescope.COMMANDS:
            for key in cmd.keys:
                await self.bind(key, cmd.action)

    async def on_mount(self, event):
        self.help_panel = HelpPanel(Telescope.COMMANDS)
        self.explorer_panel = BucketExplorerPanel(1)
        self.panel = BucketListPanel(1)
        await self.view.dock(self.panel)
        await self.view.dock(self.explorer_panel, z=1)
        await self.view.dock(self.help_panel, z=2)
        offset = -self.console.size[1]
        self.help_panel.layout_offset_y = offset
        self.explorer_panel.layout_offset_y = offset

    async def action_page_forward(self):
        panel = self.panel if not self.show_explorer else self.explorer_panel
        panel.page_forward()

    async def action_page_back(self):
        panel = self.panel if not self.show_explorer else self.explorer_panel
        panel.page_back()

    async def action_select_next(self):
        panel = self.panel if not self.show_explorer else self.explorer_panel
        panel.select_next()

    async def action_select_previous(self):
        panel = self.panel if not self.show_explorer else self.explorer_panel
        panel.select_previous()

    async def action_toggle_help(self):
        self.show_help = not self.show_help

    async def watch_show_help(self, show_help):
        y = 0 if show_help else -self.console.size[1]
        self.help_panel.animate("layout_offset_y", y)

    async def action_open_selected_item(self):
        self.explorer_panel.bucket = self.panel.item["Name"]
        self.show_explorer = True

    async def watch_show_explorer(self, show_explorer):
        self.explorer_panel.layout_offset_y = 0
