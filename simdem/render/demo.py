import random
import time


class Demo(object):
    config = None

    def __init__(self, config):
        self.config = config
        pass

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

    @staticmethod
    def display_result(res):
        """Demo specific implementation of displaying to the screen"""
        print(res, end="", flush=True)
