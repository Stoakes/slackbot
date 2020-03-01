import re
import logging
from typing import Dict

from internal.cmd.command_router import command_router
from internal.slackbot.confirm_message import ConfirmMessage


@command_router.route(
    '(.*)Hello ([a-zA-Z0-9-_]*)[ ]?(in (.*)?)?',
    match_type='regex',
    command_help='Say hello to a name, optionnally in another language',
    command_usage="Hello NAME [in LANGUAGE]",
    command_examples=["Hey bot, hello Antoine in rench"],
)
def hello(slack_message_text: str, thread_ts, regex, confirm : bool, **kwargs):
    pattern = re.compile(regex)
    result = pattern.search(slack_message_text)
    if not confirm:
        return ConfirmMessage(f"I'm going to say hello to {result.group(2)} in {result.group(4) if result.group(4) is not None else 'english'}", thread_ts) 

    if result.group(4) is not None and result.group(4) == "french":
        return "Bonjour "+ result.group(2)
    return "Hello" + result.group(2)
