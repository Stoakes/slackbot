
from internal.cmd.hello.hello import hello

class CommandsRegistry:
    """
    CommandsRegistry: is an object registering every command of your slack bot
    """

    def __init__(self):
        self.commands = []
        self.register(hello)


    def register(self, command):
        self.commands.append(command)

    def answer(self, text: str, thread_ts,  confirm: bool):
        blocks = []
        blocks.append(hello(text, thread_ts, confirm).get_content())
        blocks = self.flatten(blocks)
        
        return blocks

    def flatten(self, blocks):
        flat_blocks = []
        for item in blocks:
            if item is None:
                continue
            if isinstance(item, list):
                for b in item:
                    flat_blocks.append(b)
                continue
            flat_blocks.append(item) 
        return flat_blocks
