#!/usr/bin/env python3

import os
import logging
import slack
import ssl as ssl_lib
import certifi
import time
import sys
import datetime
import random
import string

from internal.cmd.commands_registry import CommandsRegistry
from internal.slackbot.default_message import DefaultMessage
from internal.slackbot.error_message import ErrorMessage

CHANNELS = {'#slackbot': 'PII5MAC1A'}
DEVELOPERS = {'Antoine': 'U80AB1NH0'} # Users allowed to have private chat with slackbot

registry = CommandsRegistry()

@slack.RTMClient.run_on(event="message")
def message(**payload):
    """
    Message event handler. middleware between message and command management.
    Perfect place to log and check permissions
    """

    if ("subtype" in payload["data"] and payload["data"]["subtype"] == "bot_message") or (not "text" in payload["data"]):
        # Skip reaction to a bot message or an unsupported message format (update message event for instance)
        return
    
    logging.info(payload)

    answer_blocks = registry.answer(payload["data"]["text"],payload["data"]["ts"], False)

    if len(answer_blocks) == 0:
        answer_blocks = [DefaultMessage().get_content()]

    # Post only if there's something to say
    if len(answer_blocks) > 0: 
        message = {
                "channel": payload["data"]["channel"],
                "blocks": answer_blocks,
                "text": answer_blocks[0]["text"]["text"] if ("text" in answer_blocks[0] and "text" in answer_blocks[0]["text"]) else "There's a new slackbot message", # text is required for nice slack notification
            }
        payload["web_client"].chat_postMessage(**message)

# Run on confirming an action with a green tick
@slack.RTMClient.run_on(event="reaction_added")
def confirmation_handler(**payload):
    logging.info(payload)
    if payload["data"]["reaction"] != "heavy_check_mark": # not a confirmation, ignore
        return 
    
    
    client = slack.WebClient(token=os.environ['SLACK_OAUTH_TOKEN'])
    thread = client.channels_replies(channel=payload["data"]["item"]["channel"], thread_ts=payload["data"]["item"]["ts"])

    # check if there is a red cross (which will prevent any action on this message)
    for reaction in thread["messages"][0]["reactions"]:
        if reaction["name"] == "x":
            return 
    # check if message comes from a bot and is an intent (ie describe what is going to be done) and has 2 blocks, otherwise ignore reaction
    if thread["messages"][0]["subtype"] != 'bot_message' or (not thread["messages"][0]["text"].startswith("I'm going to")) \
        or (not len(thread["messages"][0]) > 1):
        return

    # no red cross + intent bot message, update message with validation text
    msg = thread["messages"][0]
    action_id = ''.join(random.choice(string.ascii_lowercase) for i in range(6))
    msg["blocks"][1]["text"]["text"] += "\nValidated by "+payload["data"]["user"]+" on "+payload["data"]["event_ts"]+'. action id: '+action_id
    msg["channel"] = payload["data"]["item"]["channel"]
    payload["web_client"].chat_update(**msg)

    # Retrieve initial based on block id of the confirmation message (hidden in confirmation message second block' block_id)
    initial_message = client.channels_replies(channel=payload["data"]["item"]["channel"], thread_ts= msg["blocks"][1]["block_id"])
    if len(initial_message["messages"]) > 0:
        logging.debug("initial message")
        logging.debug(initial_message)

        # Process confirmation
        answer_blocks = registry.answer(initial_message["messages"][0]["text"],msg["blocks"][1]["block_id"], True)

    if answer_blocks is None or len(answer_blocks) == 0:
        answer_blocks = [ErrorMessage("Got no message to answer for "+ action_id).get_content()]

    # Post only if there's something to say
    if len(answer_blocks) > 0: 
        message = {
            "channel": payload["data"]["item"]["channel"],
            "blocks": answer_blocks,
            "text": answer_blocks[0]["text"]["text"] if ("text" in answer_blocks[0] and "text" in answer_blocks[0]["text"]) else "There's a new Opsbot message", # text is required for nice slack notification
        }
        payload["web_client"].chat_postMessage(**message)

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = os.environ["SLACK_BOT_TOKEN"]
    rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context)
    try:
        rtm_client.start()
    except slack.errors.SlackApiError as e:
        print(e)
        print("Sleeping 60 seconds before restart")
        time.sleep(60)
        sys.exit(1)
