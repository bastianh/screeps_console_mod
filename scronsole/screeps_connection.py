import json
import sys
import threading
import zlib
from time import sleep

import msgpack
import os
from base64 import b64decode
from blinker import signal
from screepsapi import screepsapi
from urwid import SPACE, LEFT

from scronsole.config_manager import ServerConfig

exit_app = signal('exit_app')


def api_client(server_config: ServerConfig):
    return screepsapi.API(server_config.user, server_config.password, server_config.ptr, server_config.host,
                          server_config.secure)


class ScreepsMessage(object):
    def __init__(self, data_tuple):
        self.type = data_tuple[0]
        self.shard = data_tuple[1]
        self.raw_data = data_tuple[2]

        self.text_attribute = None
        self.align = LEFT
        self.wrap = SPACE
        self.message = None


class Console(screepsapi.Socket):
    def __init__(self, user, password, ptr=False, logging=False, host=None, secure=None, pipe=None):
        self.pipe = pipe
        exit_app.connect(self.exit)
        super(Console, self).__init__(user, password, ptr, logging, host, secure)

    def send_pipe(self, data):
        os.write(self.pipe, msgpack.packb(data, use_bin_type=True) + b'\0')

    def process_cpu(self, ws, data):
        self.send_pipe({"cpu": data})

    def on_message(self, ws, message):
        if message.startswith('auth ok'):
            self.set_subscriptions()
            return

        if message.startswith('time'):
            return

        if message.startswith('gz'):
            try:
                decoded = b64decode(message[3:])
                message = zlib.decompress(decoded, 0)
            except:
                print("Unexpected error:", sys.exc_info())
                return
        data = json.loads(message)

        if 'shard' in data[1]:
            shard = data[1]['shard']
        else:
            shard = 'shard0'

        if 'messages' in data[1]:
            stream = []

            if 'log' in data[1]['messages']:
                stream = stream + data[1]['messages']['log']

            if 'results' in data[1]['messages']:
                results = data[1]['messages']['results']
                if len(results):
                    for row in results:
                        self.send_pipe(('result', shard, row))

            message_count = len(stream)

            if message_count > 0:
                # config = settings.getSettings()
                # Make sure the delay doesn't cause an overlap into other ticks
                # if 'smooth_scroll' in config and config['smooth_scroll'] is True:
                if 1:
                    message_delay = 0.2 / message_count
                    if message_delay > 0.07:
                        message_delay = 0.07
                else:
                    message_delay = 0.00001

                for line in stream:
                    self.send_pipe(('log', shard, line))
                    sleep(message_delay)
            return
        else:
            if 'error' in data[1]:
                line = data[1]['error']
                self.send_pipe(('error', shard, line))
                return
            else:
                self.send_pipe(('unknown', shard, message))

    def on_close(self, ws):
        super(Console, self).on_close(ws)

    def set_subscriptions(self):
        super(Console, self).set_subscriptions()
        self.subscribe('server-message')
        self.subscribe_user('console')
        self.subscribe_user('cpu')
        # self.subscribe_user('money')

    def exit(self, sender):
        self.disconnect()


class ScreepsConnection(threading.Thread):
    def __init__(self, pipe, serverconfig: ServerConfig):
        threading.Thread.__init__(self)
        self.pipe = pipe
        self.server_config = serverconfig

    def run(self):
        screepsconsole = Console(user=self.server_config.user, password=self.server_config.password,
                                 host=self.server_config.host, secure=self.server_config.secure,
                                 ptr=self.server_config.ptr, pipe=self.pipe)
        screepsconsole.start()
        screepsconsole.send_pipe("exit")
        os.close(self.pipe)
