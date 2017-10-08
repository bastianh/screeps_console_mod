import urwid


class ConsoleListWalker(urwid.SimpleListWalker):
    def set_modified_callback(self, callback):
        raise NotImplementedError('Use connect_signal('
                                  'list_walker, "modified", ...) instead.')

    def __init__(self, contents):
        self.max_buffer = 20000
        super().__init__(contents)

    def appendText(self, value, style=None):
        if style:
            return self.append(urwid.Text((style, value,)))
        return self.append(urwid.Text(value))

    def append(self, value):
        if len(self) >= self.max_buffer:
            self.pop(0)

        return super().append(value)
