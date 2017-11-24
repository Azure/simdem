import time
import random

from .. import helpers,executor
from .. import config

class Demo(object):
    exe = None

    def __init__(self):
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

        print(config.CONSOLE_PROMPT, end="", flush=True)
        for idx, char in enumerate(cmd):
            if char != "\n":
                if config.TYPING_DELAY:
                    delay = random.uniform(0.02, config.TYPING_DELAY)
                    time.sleep(delay)
                print(char, end="", flush=True)
        print("", flush=True)

    def display_result(self, res):
        print(res, end="", flush=True)
