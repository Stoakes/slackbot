from typing import List

class ErrorMessage:
    """
    ErrorMessage: a message to use when there is an error.
    """
    def __init__(self, error: str):
        self.error = error
    
    def get_content(self):
        return {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"ERROR\n\n{self.error}"
                }
            }