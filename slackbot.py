#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A slackbot that responds to commands.
This uses the Slack RTM (Real Time Messaging) API.
Required environment variables (example only, these are not real tokens).
Get these from the Slack account settings that you are connecting to.
   BOT_USER_ID = 'U20981S736'
   BOT_USER_TOKEN = 'xoxb-106076235608-AbacukynpGahsicJqugKZC'
"""

import logging
import signal
import time
from slackclient import SlackClient

__author__ = 'dougenas and mpmckenz'
BOT_NAME = 'Spotbot'
BOT_CHAN = '#bot-test'

still_running = True
logger = logging.getLogger(__name__)
loop_int = 5

bot_commands = {
    'help':  'Shows this helpful command reference.',
    'ping':  'Show uptime of this bot.',
    'exit':  'Shutdown the entire bot (requires app restart)',
    'raise':  'Manually test exception handler'
}

def formatted_dict(d, k_header='Keys', v_header='Values'):
    """Renders contents of a dict into a preformatted string"""
    if d:
        lines = []
        # find the longest key entry in d or the key header string
        width = max(map(len, d))
        width = max(width, len(k_header))
        lines.extend(['{k:<{w}} : {v}'.format(k=k_header, v=v_header, w=width)])
        lines.extend(['-'*width + '   ' + '-'*len(v_header)])
        lines.extend('{k:<{w}} : {v}'.format(k=k, v=v, w=width) for k, v in d.items())
        return '\n'.join(lines)
    return "<empty>"

print(formatted_dict(bot_commands, k_header="My cmds", v_header='What they do'))

def config_logger():
    """Setup logging configuration"""
    global logger
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s:%(message)s')
    file_handler = logging.FileHandler("filelog.log")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def command_loop(bot):
    """Process incoming bot commands"""
    print("This is a test")
    # pass


def signal_handler(sig_num, frame):
    global logger
    logger.info("signal number: {}".format(sig_num))
    if sig_num == 5:
        global still_running
        still_running = False
    pass


class SlackBot:

    def __init__(self, bot_user_token, bot_id=None):
        """Create a client instance"""
        pass

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def __enter__(self):
        """Implement this method to make this a context manager"""
        pass

    def __exit__(self, type, value, traceback):
        """Implement this method to make this a context manager"""
        pass

    def post_message(self, msg, chan=BOT_CHAN):
        """Sends a message to a Slack Channel"""
        pass

    def handle_command(self, raw_cmd, channel):
        """Parses a raw command string from the bot"""
        pass


def main():
    config_logger()
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    while still_running:
        # command_loop(bot)
        time.sleep(loop_int)
    pass


if __name__ == '__main__':
    main()
