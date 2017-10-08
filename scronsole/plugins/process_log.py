import re

TAG_RE = re.compile(r'<[^>]+>')


# noinspection PyBroadException
def process_message(_sender, screeps_message, **_kwargs):
    if screeps_message.type == "log":
        try:
            screeps_message.message = TAG_RE.sub('', screeps_message.raw_data)
        except:
            screeps_message.message = screeps_message.raw_data


def setup(plugin_manager):
    plugin_manager.register_process_message(process_message)
    # pass
