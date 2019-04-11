#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dotenv import load_dotenv
from spotbot import artist_top_10, sp, get_playlists, search_tool
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
import os
from slackclient import SlackClient
<< << << < Updated upstream
== == == =
>>>>>> > Stashed changes

__author__ = 'dougenas and mpmckenz'
BOT_NAME = 'Spotbot'
BOT_CHAN = '#bot-test'

still_running = True
logger = logging.getLogger(__name__)
loop_int = 5
slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)

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
        lines.extend(['{k:<{w}} : {v}'.format(
            k=k_header, v=v_header, w=width)])
        lines.extend(['-'*width + '   ' + '-'*len(v_header)])
        lines.extend('{k:<{w}} : {v}'.format(k=k, v=v, w=width)
                     for k, v in d.items())
        return '\n'.join(lines)
    return "<empty>"


print(formatted_dict(bot_commands, k_header="My cmds", v_header='What they do'))


def config_logger():
    """Setup logging configuration"""
    global logger
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s:%(message)s')
    file_handler = logging.FileHandler("spotbot.log")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def command_loop(bot):
    """Process incoming bot commands"""


<< << << < Updated upstream
    print("This is a test")
    # pass

== == == =
    HELP = "help"
    STAIRWAY = "stairway"
    PLAYLIST = "playlist"
    RAISE = "raise"
    LOGOUT = "logout"
    PING = "ping"
    FUNPLAYLIST = "fun"

    global stay_running

    command, channel = bot.parse_bot_commands(bot.slack_client.rtm_read())
    if command:
        if command == HELP:
            bot.help(channel)
        elif command == STAIRWAY:
            bot.stairway(channel)
        elif command == PLAYLIST:
            bot.playlist(channel)
        elif command == LOGOUT:
            stay_running = False
            bot.logout(channel)
            logger.info('User initiated command: {}'.format(command))
        elif command == RAISE:
            raise CustomError("What did you do?")
        elif command == PING:
            bot.ping(channel)
        elif command == FUNPLAYLIST:
            bot.fun(channel)


class CustomError(Exception):
    pass


def signal_handler(sig_num, frame):
    global stay_running
    sigs = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items()))
                if v.startswith('SIG') and not v.startswith('SIG_'))
    logger.warning('Received OS Signal: {}'.format(sigs[sig_num]))


>>>>>> > Stashed changes


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

        )

    def help(self, channel):
        message="Try these commands: stairway | playlist | logout | ping | help | fun"
        self.post_message(message, channel)

    def __enter__(self):
        """Implement this method to make this a context manager"""
        pass

    def __exit__(self, type, value, traceback):
        """Implement this method to make this a context manager"""
        pass

    def fun(self, channel):
        info=search_tool(sp)
        self.post_message(info, channel)

    def logout(self, channel):
        message="Spotbot has logged off"
        self.post_message(message, channel)

        pass

    def handle_command(self, raw_cmd, channel):
        """Parses a raw command string from the bot"""
        pass

def main():
    config_logger()
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    bot=SlackBot(slack_token)

    if bot.slack_client.rtm_connect(with_team_state = False):
        bot.post_message(ONLINE, BOT_CHAN)
        logger.info("Spotbot initialized!")
        while stay_running:
            command_loop(bot)
            time.sleep(loop_int)


if __name__ == '__main__':
    main()
