import urwid


class ConsoleWidget(urwid.ListBox):
    _autoscroll = True

    @property
    def autoscroll(self):
        return self._autoscroll

    @autoscroll.setter
    def autoscroll(self, value):
        self._autoscroll = value

    def execute_autoscroll(self):
        if (self._autoscroll):
            self.scrollBottom()

    def scrollBottom(self):
        self._autoscroll = True
        if len(self.body) > 0:
            self.set_focus(len(self.body) - 1)

    def scrollUp(self, quantity):
        self._autoscroll = False
        new_pos = self.focus_position - quantity
        if new_pos < 0:
            new_pos = 0
        self.set_focus(new_pos)

    def scrollDown(self, quantity):
        self._autoscroll = False
        max_pos = len(self.body) - 1
        new_pos = self.focus_position + quantity
        if new_pos > max_pos:
            self._autoscroll = True
            new_pos = max_pos
        self.set_focus(new_pos)
