import urwid

from scronsole.config_manager import ConfigManager
from scronsole.plugin_manager import PluginManager
from scronsole.widgets.main_menu import MainMenu
from scronsole.widgets.server_screen import ServerScreen


class MainScreen(urwid.WidgetPlaceholder):
    def __init__(self):
        super().__init__(urwid.SolidFill(u'/'))
        self.config = ConfigManager()
        self.show_main_menu()
        self.plugins = PluginManager(self)
        self.plugins.load_plugins()

    def show_server_screen(self, server_data):
        self.original_widget = ServerScreen(self, server_data)

    def show_main_menu(self):
        self.original_widget = MainMenu(self)
