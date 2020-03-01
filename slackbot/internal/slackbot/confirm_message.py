
class ConfirmMessage:
    """
    ConfirmMessage: Message type to use when looking for a confirmation
    """
    def __init__(self, confirm_string: str, thread_ts: str):
        self.confirm = confirm_string
        self.thread_ts = thread_ts
    
    def get_content(self):
        return  [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{self.confirm}"
                    }
                },
                {
                "type": "section",
                "block_id": f"{self.thread_ts}", # this id will be used by confirmation handler to know which message refering to.
                "text": {
                    "type": "mrkdwn",
                    "text": "Confirm by adding a :heavy_check_mark: reaction. Deny by adding a :x:"
                }
            },
            ]
