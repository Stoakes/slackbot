
import logging
import pprint
import re
from internal.slackbot.help_message import HelpMessage
from internal.slackbot.empty_message import EmptyMessage
from internal.slackbot.string_message import StringMessage


class CommandRouter:

    def route(self, regex, **kwargs):
        def parameter_router(fonction_a_executer):
            """"""
            def fonction_modifiee(slack_message_text: str, thread_ts, confirm: bool):
                if "help" in slack_message_text:
                    return HelpMessage( 
                        kwargs.get("command_usage", "No command usage defined"),
                        kwargs.get("command_help", "No help defined"),
                        kwargs.get("command_examples", [""])
                        )
                if not re.match(regex, slack_message_text):
                    logging.debug(slack_message_text + " does not matches "+ regex)
                    return EmptyMessage()

                result = fonction_a_executer(slack_message_text, thread_ts, regex, confirm)
                logging.debug(result)
                if type(result) is str:
                    return StringMessage(result)
                
                return result # Assuming this is a valid message
            return fonction_modifiee
        return parameter_router


command_router = CommandRouter()
