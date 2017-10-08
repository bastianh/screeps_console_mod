def command_gcl(api_client, listwalker, **kwargs):
    control_points = int(api_client.me()['gcl'])
    gcl = str(int((control_points / 1000000) ** (1 / 2.4)) + 1)
    listwalker.appendText(gcl, style='logged_response')


def command_pause(listbox, **kwargs):
    listbox.autoscroll = False


def command_turtle(listwalker, **kwargs):
    turtle = '''
 ________________
< How you doing? >
 ----------------
    \                                  ___-------___
     \                             _-~~             ~~-_
      \                         _-~                    /~-_
             /^\__/^\         /~  \                   /    \\
           /|  O|| O|        /      \_______________/        \\
          | |___||__|      /       /                \          \\
          |          \    /      /                    \          \\
          |   (_______) /______/                        \_________ \\
          |         / /         \                      /            \\
           \         \^\\\         \                  /               \     /
             \         ||           \______________/      _-_       //\__//
               \       ||------_-~~-_ ------------- \ --/~   ~\    || __/
                 ~-----||====/~     |==================|       |/~~~~~
                  (_(__/  ./     /                    \_\      \.
                         (_(___/                         \_____)_)
'''
    listwalker.appendText(turtle)
    listwalker.appendText('')


def command_whoami(api_client, listwalker, **kwargs):
    me = api_client.me()['username']
    listwalker.appendText(me, style='logged_response')


# noinspection PyCallingNonCallable
def process_edit_text(*args, editbar, listbox, listwalker, **kwargs):
    edit_text = editbar.get_edit_text()
    user_command_split = edit_text.split(' ')
    first_command = user_command_split[0]
    func = globals().get("command_%s" % first_command)
    if func:
        listwalker.appendText('> ' + edit_text, style='logged_input')
        func(editbar=editbar,
             listbox=listbox,
             listwalker=listwalker,
             command_rest=" ".join(user_command_split[1:]),
             **kwargs)
        listbox.execute_autoscroll()
        editbar.set_edit_text('')
        return True


def setup(plugin_manager):
    plugin_manager.register_process_command(process_edit_text)
