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

__author__ = 'dougenas and mpmckenz'

import logging
import signal
import time
import os
import re
from slackclient import SlackClient
from spotbot import artist_top_10, sp, get_playlists, search_tool
from dotenv import load_dotenv

BOT_NAME = 'spotify_bot'
BOT_CHAN = 'CCD7MHJD8'

stay_running = True
logger = logging.getLogger(__name__)
loop_int = 2
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

env_path = os.path.join('./', '.env')
load_dotenv(dotenv_path=env_path, verbose=True, override=True)

slack_token = os.getenv('SLACK_API_TOKEN')


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


def command_loop(bot):

    """Process incoming bot commands"""
    HELP = "help"
    STAIRWAY = "stairway"
    PLAYLIST = "playlist"
    RAISE = "raise"
    LOGOUT = "logout"
    PING = "ping"
    EXCEPTION = "You raised an error"
    DEFAULT = "Not sure what you mean. Try 'help' to see a list of usable commands"
    FUNPLAYLIST = "fun"

    global stay_running

    command, channel = bot.parse_bot_commands(bot.slack_client.rtm_read())
    if command:
        # print("channel is {}".format(channel))
        log = logger.info('User initiated command: {}'.format(command))
        if command == HELP:
            bot.help(channel)
            log
        elif command == STAIRWAY:
            bot.stairway(channel)
            log
        elif command == PLAYLIST:
            bot.playlist(channel)
            log
        elif command == LOGOUT:
            stay_running = False
            bot.logout(channel)
            log
        elif command == RAISE:
            raise CustomError(EXCEPTION)
        elif command == PING:
            bot.ping(channel)
            log
        elif command == FUNPLAYLIST:
            bot.fun(channel)
            log
        else:
            bot.post_message(DEFAULT, channel)


class CustomError(Exception):
    pass


def signal_handler(sig_num, frame):
    global stay_running
    sigs = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items()))
                if v.startswith('SIG') and not v.startswith('SIG_'))
    logger.warning('Received OS Signal: {}'.format(sigs[sig_num]))

    stay_running = False
    pass


class SlackBot:

    def __init__(self, bot_user_token, bot_id=None):
        """Create a client instance"""
        self.slack_client = SlackClient(bot_user_token)
        self.bot_name = BOT_NAME
        self.bot_id = self.get_bot_id()
        self.start_time = time.time()

        if self.bot_id is None:
            exit("Error, could not find " + str(self.bot_name))

    def get_bot_id(self):
        api_call = self.slack_client.api_call("users.list")
        if api_call.get('ok'):
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == self.bot_name:

                    return user.get('id')
            return None

    def parse_bot_commands(self, slack_events):
        for event in slack_events:
            if event.get("type") == "message" and not "subtype" in event:
                user_id, message = self.parse_direct_mention(event.get("text"))
                print(user_id, self.bot_id)
                if user_id == self.bot_id:
                    return message, event.get("channel")
        return None, None

    def parse_direct_mention(self, message_text):
        matches = re.search(MENTION_REGEX, message_text)
        if matches:
            return matches.group(1), matches.group(2).strip()
        else:
            return (None, None)

    def post_message(self, msg, channel):
        """Sends a message to a Slack Channel"""
        self.slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=msg

        )
    def help(self, channel):
        message = "Try these commands: stairway | playlist | fun | logout | ping | help"
        self.post_message(message, channel)

    def stairway(self, channel):
        info = artist_top_10(sp)
        self.post_message(info, channel)

    def playlist(self, channel):
        info = get_playlists(sp)
        self.post_message(info, channel)

    def fun(self, channel):
        info = search_tool(sp)
        self.post_message(info, channel)

    def logout(self, channel):
        message = "Spotbot has logged off"
        self.post_message(message, channel)

    def ping(self, channel):
        start_time = time.strftime(
            '%H:%M:%S', time.localtime(self.start_time)
            )
        message = "Spotbot Uptime: Bot has been online since {}".format(start_time)
        self.post_message(message, channel)



def main():
    ONLINE = "Spotbot is online"
    config_logger()
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    bot = SlackBot(slack_token)
    
    if bot.slack_client.rtm_connect(with_team_state=False):
        logger.info("Spotbot initialized!")
        bot.post_message(ONLINE, BOT_CHAN)
        while stay_running:
            command_loop(bot)
            time.sleep(loop_int)


if __name__ == '__main__':
    main()
