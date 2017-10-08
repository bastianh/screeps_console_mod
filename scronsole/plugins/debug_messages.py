import re

TAG_RE = re.compile(r'<[^>]+>')


# noinspection PyBroadException
def process_message(_sender, screeps_message, **_kwargs):
    if screeps_message.type not in ["log", "error", "result"]:
        screeps_message.message = TAG_RE.sub('', screeps_message.raw_data)
        try:
            screeps_message.message = str(screeps_message.type) + ":" + TAG_RE.sub('', screeps_message.raw_data)
        except:
            screeps_message.message = str(screeps_message.type) + ":" + str(screeps_message.raw_data)


def setup(plugin_manager):
    pass
    # plugin_manager.register_process_message(process_message)
