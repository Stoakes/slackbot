from typing import List

class DefaultMessage:
    """
    DefaultMessage: a message to use when nothing has been found to be done.
    """
    def __init__(self):
        pass
    
    def get_content(self):
        return {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": """The previous message does not match any command. Type `help` to get details about what I can do"""
                }
            }