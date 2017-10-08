import re

SEVERITY_RE = re.compile(r'<.*severity="(\d)".*>')


# noinspection PyBroadException
def get_severity(line):
    if '<' in line:
        try:
            match_return = SEVERITY_RE.match(line)
            groups = match_return.groups()
            if len(groups) > 0:
                return int(groups[0])
            else:
                return 3
        except:
            return 3
    else:
        return 3


# noinspection PyBroadException
def post_process_message(_sender, screeps_message, **_kwargs):
    if screeps_message.type == "log":
        screeps_message.text_attribute = 'severity_%d' % get_severity(screeps_message.raw_data)


def setup(plugin_manager):
    plugin_manager.register_post_process_message(post_process_message)
