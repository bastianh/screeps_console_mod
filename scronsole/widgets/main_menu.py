from typing import TYPE_CHECKING

import urwid

if TYPE_CHECKING:
    from scronsole.widgets.main_screen import MainScreen


class MainMenu(urwid.WidgetWrap):
    def item_chosen(self, _button, user_info):
        self.main_screen.show_server_screen(user_info)

    def __init__(self, main_screen: "MainScreen"):
        super().__init__("")
        self.main_screen = main_screen
        choices = main_screen.config.get_servers()
        body = [urwid.Text("Server"), urwid.Divider()]
        for c in choices:
            label = c.host
            if not label:
                label = "screeps.com"
                if c.ptr:
                    label += " (ptr)"
            button = urwid.Button(label)
            urwid.connect_signal(button, 'click', self.item_chosen, c)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))

        box = urwid.LineBox(urwid.ListBox(urwid.SimpleFocusListWalker(body)))
        self._w = urwid.Overlay(box, urwid.SolidFill(u'\N{MEDIUM SHADE}'), align='center', width=('relative', 50),
                                valign='middle', height=('relative', 50),
                                min_width=20, min_height=4)
