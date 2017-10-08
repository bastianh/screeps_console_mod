#!/usr/bin/env python3
import click
import urwid

from scronsole.screeps_connection import exit_app
from scronsole.widgets.main_screen import MainScreen


@click.command()
@click.option('--debug', is_flag=True, help='Connect to debugger')
def start(debug):
    if debug:
        import pydevd
        pydevd.settrace('localhost', port=24423, stdoutToServer=True, stderrToServer=True, suspend=False)

    top = MainScreen()
    loop = urwid.MainLoop(top, palette=[
        ('reversed', 'standout', ''),

        ('severity_1', 'dark cyan', ''),
        ('severity_2', 'dark green', ''),
        ('severity_3', '', ''),
        ('severity_4', 'yellow', ''),
        ('severity_5', 'dark red', ''),

        ('input', 'white', 'dark blue'),
        ('header', 'white', 'dark blue'),
        ('logged_response', 'light magenta', 'black'),
        ('error_message', 'yellow', 'dark red'),
    ])
    top.event_loop = loop
    try:
        loop.run()
    except KeyboardInterrupt:
        exit_app.send()
        exit(0)


if __name__ == "__main__":
    start()
