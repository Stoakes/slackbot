from typing import List

class HelpMessage:
    """
    HelpMessage: a help message is the result of a help request.
    This helps having a consistent output for help commands.
    """
    def __init__(self, command_usage: str, command_help: str, command_examples: List):
        self.usage = command_usage
        self.help = command_help
        self.examples = command_examples
    
    def get_content(self):
        example_string = ""
        for example in self.examples:
            example_string += "`"+example+"`\n"
        return {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"""*{self.usage}*
                    {self.help}
                    {example_string}
                    """
                }
            }