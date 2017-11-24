import time
import random

from .. import helpers,executor

class Demo(object):
    exe = None
    config = None

    def __init__(self, config):
        self.config = config
        self.exe = executor.Executor()
        pass

    def run_cmd(self, cmd):
        self.type_command(cmd)
        res = self.exe.run_cmd(cmd)
        self.display_result(res)
        return res

    def type_command(self, cmd):
        """
        Displays the command on the screen
        """

        # Must add ' ' when typing command because whitespaces are removed from configparser
        # https://docs.python.org/3/library/configparser.html#supported-ini-file-structure
        print(self.config.get('RENDER', 'CONSOLE_PROMPT', raw=True) + ' ', end="", flush=True)
        for idx, char in enumerate(cmd):
            if char != "\n":
                typing_delay = float(self.config.get('RENDER', 'TYPING_DELAY'))
                if typing_delay:
                    delay = random.uniform(0.02, typing_delay)
                    time.sleep(delay)
                print(char, end="", flush=True)
        print("", flush=True)

    def display_result(self, res):
        print(res, end="", flush=True)
