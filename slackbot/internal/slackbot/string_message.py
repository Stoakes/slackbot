class StringMessage:
    """
    StringMessage: The type to use when a function only returns a string
    """
    def __init__(self, result_string: str):
        self.result = result_string
    
    def get_content(self):
        return {
                "type": "section",
                "text": {
                "type": "mrkdwn",
                "text": f"""{self.result}"""
                }
            }