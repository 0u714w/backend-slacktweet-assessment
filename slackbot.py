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
from dotenv import load_dotenv

BOT_NAME = 'spotify_bot'
BOT_CHAN = '#bot-test'
bot_id = None

stay_running = True
logger = logging.getLogger(__name__)
loop_int = 5
env_path = os.path.join('./', '.env')
load_dotenv(dotenv_path=env_path, verbose=True, override=True)
slack_token = os.getenv('SLACK_API_TOKEN')
sc = SlackClient(slack_token)


RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


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
    file_handler = logging.FileHandler("spotbot.log")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def command_loop(bot):
    """Process incoming bot commands"""
    command, channel = bot.parse_bot_commands(bot.slack_client.rtm_read())
    if command:
        message = "test 1 2 3"
        bot.post_message(message, channel)
        print(command, channel)
    


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
        print(slack_events)
        for event in slack_events:
            if event.get("type") == "message" and not "subtype" in event:
                user_id, message = self.parse_direct_mention(event.get("text"))
                print(user_id, self.bot_id)
                if user_id == self.bot_id:
                    print("inside logic")
                    return message, event.get("channel")
        return None, None

    def parse_direct_mention(self, message_text):
        matches = re.search(MENTION_REGEX, message_text)
        if matches:
            return matches.group(1), matches.group(2).strip()
        else:
            return (None, None)

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

    def post_message(self, msg, channel):
        """Sends a message to a Slack Channel"""
        self.slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=msg
        )
       

    def handle_command(self, raw_cmd, channel):
        """Parses a raw command string from the bot"""
        pass



def main():
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
