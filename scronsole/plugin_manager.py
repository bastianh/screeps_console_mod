import os
from typing import TYPE_CHECKING

from blinker import signal
from pluginbase import PluginBase

if TYPE_CHECKING:
    from scronsole.widgets.main_screen import MainScreen

plugin_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugins")

signal_pre_process_message = signal('pre_process_message')
signal_process_message = signal('process_message')
signal_post_process_message = signal('post_process_message')

signal_process_command = signal('signal_process_command')

class PluginManager(object):
    def __init__(self, main_screen: "MainScreen"):
        self.base = PluginBase(package='scronsole.plugins')
        self.source = self.base.make_plugin_source(searchpath=['./path/to/plugins', plugin_dir])

    def load_plugins(self):
        with self.source:
            for name in self.source.list_plugins():
                plugin = self.source.load_plugin(name)
                plugin.setup(self)

    def register_process_command(self, handler):
        signal_process_command.connect(handler, weak=True)

    def register_process_message(self, handler):
        signal_process_message.connect(handler, weak=True)

    def register_pre_process_message(self, handler):
        signal_pre_process_message.connect(handler, weak=True)

    def register_post_process_message(self, handler):
        signal_post_process_message.connect(handler, weak=True)

        # def register_hook(self, name, handler):
        #     signal(name).connect(handler, weak=True)
