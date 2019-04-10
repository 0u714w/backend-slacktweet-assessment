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
from spotbot import artist_top_10, sp, get_playlists
from dotenv import load_dotenv

BOT_NAME = 'spotify_bot'
BOT_CHAN = '#bot-test'
bot_id = None

stay_running = True
logger = logging.getLogger(__name__)
loop_int = 2

env_path = os.path.join('./', '.env')
load_dotenv(dotenv_path=env_path, verbose=True, override=True)

slack_token = os.getenv('SLACK_API_TOKEN')
sc = SlackClient(slack_token)

RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


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
    
    command, channel = bot.parse_bot_commands(bot.slack_client.rtm_read())
    sc.rtm_connect()
    if command:
        cmd = handle_command(command)
        post_message(cmd, channel)


class CustomError(Exception):
    pass

def handle_command(command):
    """
        Interpret commands and send them to execute_command
    """
    response = None
    HELP = "-help"
    LED = "led"
    PLAYLIST = "playlist"
    RAISE = "raise"
    LOGOUT = "logout"


    # This is where you start to implement more commands!
    global stay_running
    if not command:
        response = "Spotpot is online"
    if command.startswith(RAISE):
        raise CustomError("what happened???")
    if command.startswith(HELP):
        response = "Try these commands: led / playlist"
    if command.startswith(LED):
        response = artist_top_10(sp)
    if command.startswith(PLAYLIST):
        response = get_playlists(sp)
    if command.startswith(LOGOUT):
        stay_running = False
        response = "Exiting..."
        logger.info("Connection terminated by user's exit command.")
    logger.info('User initiated command: {}'.format(command))
    return response



def signal_handler(sig_num, frame):
    global stay_running
    sigs = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items()))
                if v.startswith('SIG') and not v.startswith('SIG_'))
    logger.warning('Received OS Signal: {}'.format(sigs[sig_num]))

    stay_running = False
    pass

def post_message(msg, channel):
    """Sends a message to a Slack Channel"""
    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=msg
        )

class SlackBot:

    def __init__(self, bot_user_token, bot_id=None):
        """Create a client instance"""
        self.slack_client = SlackClient(bot_user_token)
        self.bot_name = BOT_NAME
        self.bot_id = self.get_bot_id()

        if self.bot_id is None:
            exit("Error, could not find " + str(self.bot_name))

    def get_bot_id(self):
        api_call = self.slack_client.api_call("users.list")
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == self.bot_name:
                    # return "<@" + user.get('id') + ">"
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


def main():
    ONLINE = "Spotbot is online"
    config_logger()
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    bot = SlackBot(slack_token)
    
    if bot.slack_client.rtm_connect(with_team_state=False):
        logger.info("Spotbot initialized!")
        while stay_running:
            command_loop(bot)
            time.sleep(loop_int)

        
    pass


if __name__ == '__main__':
    main()
