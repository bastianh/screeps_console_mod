import msgpack
import urwid

from scronsole.plugin_manager import signal_process_message, signal_post_process_message, signal_pre_process_message, \
    signal_process_command
from scronsole.screeps_connection import ScreepsConnection, api_client, ScreepsMessage
from scronsole.widgets.console_list_walker import ConsoleListWalker
from scronsole.widgets.console_widget import ConsoleWidget
from scronsole.widgets.edit_bar import EditBar


class HeaderBar(urwid.WidgetWrap):
    def __init__(self, screen: "ServerScreen"):
        super().__init__("")
        self.screen = screen
        self._w = urwid.AttrMap(urwid.Text("SCRONSOLE", align='center'), 'header')


class ServerScreen(urwid.WidgetWrap):
    buffer = b''
    api_connection = None

    def pipe_action(self, data):
        self.buffer += data
        if len(self.buffer) and self.buffer[-1] == 0:
            for row in self.buffer.split(b'\0'):
                if len(row) == 0:
                    continue
                received = msgpack.unpackb(row, encoding='utf-8', use_list=False)
                if type(received) == tuple:
                    message = ScreepsMessage(received)
                    signal_pre_process_message.send(self, screeps_message=message)
                    signal_process_message.send(self, screeps_message=message)
                    if message.message:
                        signal_post_process_message.send(self, screeps_message=message)
                        widget = urwid.Text(message.message, align=message.align, wrap=message.wrap)
                        if message.text_attribute:
                            widget = urwid.AttrMap(widget, message.text_attribute)
                        self.listwalker.append(widget)
                        self.listbox.execute_autoscroll()
                else:
                    self.listwalker.append(urwid.Text(str(received) + "  %r" % len(data)))
            self.buffer = b''
        return True

    def on_command(self):
        self.listbox.autoscroll = True

        if self.api_connection is None:
            self.api_connection = api_client(self.server_config)

        # call signal to let plugins process the command
        back = signal_process_command.send(listbox=self.listbox,
                                           listwalker=self.listwalker,
                                           editbar=self.editbar,
                                           api_client=self.api_connection)

        # stop if a plugin processed the command
        for (f, result) in back:
            if result:
                return

        # Send command to Screeps API. Output will come from the console stream.
        user_input = self.editbar
        user_text = user_input.get_edit_text()

        if len(user_text) > 0:
            self.listwalker.append(
                urwid.Text(('logged_input', '> ' + user_text)))
            self.listbox.scrollBottom()
            user_input.set_edit_text('')
            self.api_connection.console(user_text, "shard1")

    def keypress(self, _size, key):

        # lastkeytime = self.keypress.lastkeytime
        # self.keypress.lastkeytime = calendar.timegm(time.gmtime())
        #
        # if self.keypress.lastkeytime - lastkeytime > 1:
        #     self.keypress.last_key = None
        #
        # lastkey = self.keypress.last_key
        # self.keypress.last_key = key
        super().keypress(_size, key)

        #        if not self.listwalker:
        #            return

        if key == 'enter':
            self.on_command()

        elif key == 'tab':
            pass

        elif key == 'page up':
            info = self.loop.screen.get_cols_rows()
            self.listbox.scrollUp(int(info[1] / 3))

        elif key == 'page down':
            info = self.loop.screen.get_cols_rows()
            self.listbox.scrollDown(int(info[1] / 3))

        elif key == 'meta up':
            self.listbox.scrollUp(1)

        elif key == 'meta down':
            self.listbox.scrollDown(1)

    def start_connection(self):
        pipe = self.main_screen.event_loop.watch_pipe(self.pipe_action)
        self.screeps_connection = ScreepsConnection(pipe, serverconfig=self.server_config)
        self.screeps_connection.start()

    def __init__(self, main_screen, server_config):
        super().__init__("")
        self.screeps_connection = None
        self.server_config = server_config
        self.main_screen = main_screen

        self.header = HeaderBar(self)
        self.listwalker = ConsoleListWalker([])
        self.listbox = ConsoleWidget(self.listwalker)
        self.editbar = EditBar(caption="> ")

        self._w = urwid.Frame(body=self.listbox, header=self.header, footer=urwid.AttrMap(self.editbar, 'input'),
                              focus_part='footer')

        self.start_connection()
