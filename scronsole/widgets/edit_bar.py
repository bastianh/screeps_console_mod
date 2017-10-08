import os

import urwid


class EditBar(urwid.Edit):
    inputBuffer = []
    inputOffset = 0

    def __init__(self, **kwargs):
        path = os.path.expanduser('~') + '/.screeps_history'
        if os.path.isfile(path):
            with open(path, 'r') as myfile:
                file_contents = myfile.read()
                self.inputBuffer = file_contents.splitlines()
                self.inputBuffer.reverse()
        super().__init__(**kwargs)

    def bufferInput(self, text):
        if len(text) < 1:
            return
        path = os.path.expanduser('~') + '/.screeps_history'
        history_file = open(path, 'a')
        history_file.write(text + "\n")
        self.inputBuffer.insert(0, text)
        self.manageBufferHistory()

    def manageBufferHistory(self):
        path = os.path.expanduser('~') + '/.screeps_history'
        with open(path, 'r') as myfile:
            file_contents = myfile.read()
            file_contents_line = file_contents.splitlines()
            num_lines = len(file_contents_line)
            # config = settings.getSettings()
            # if 'max_history' in config:
            #    max_scroll = config['max_history']
            # else:
            max_scroll = 200000

            if num_lines > max_scroll:
                truncate = num_lines - max_scroll
                list_copy = file_contents_line[:]
                list_copy = [s + "\n" for s in list_copy]
                open(path, 'w').writelines(list_copy[truncate + 1:])

    def keypress(self, size, key):

        if key == 'enter':
            edit_text = self.get_edit_text()
            self.bufferInput(edit_text)
            self.inputOffset = 0
            return super().keypress(size, key)

        if key == 'ctrl a':
            self.edit_pos = 0
            return

        if key == 'ctrl e':
            edit_text = self.get_edit_text()
            self.edit_pos = len(edit_text)
            return

        if key == 'ctrl u':
            self.set_edit_text('')
            self.edit_pos = 0
            return

        if key == 'up':
            bufferLength = len(self.inputBuffer)
            if bufferLength > 0:
                self.inputOffset += 1
                if self.inputOffset > bufferLength:
                    self.inputOffset = bufferLength

                index = self.inputOffset - 1
                new_text = self.inputBuffer[index]
                self.set_edit_text(new_text)
                self.edit_pos = len(new_text)
            return

        if key == 'down':
            bufferLength = len(self.inputBuffer)
            if bufferLength > 0:
                self.inputOffset -= 1
                if self.inputOffset < 0:
                    self.inputOffset = 0

                if self.inputOffset == 0:
                    new_text = ''
                else:
                    index = self.inputOffset - 1
                    new_text = self.inputBuffer[index]

                self.set_edit_text(new_text)
                self.edit_pos = len(new_text)
            return

        return super().keypress(size, key)
