"""Demo (default) mode for SimDem"""

import random
import time
import logging
from simdem.mode.common import ModeCommon

class DemoMode(ModeCommon):
    """ This class is the default SimDem file processor.
        It's designed for running files in a demo-able mode that looks like a human is typing it
    """

    def process(self, steps):
        """ Processes the steps from a processed file """
        logging.debug("process()")

        for step in steps['body']:
            if step['type'] == 'commands':
                self.process_commands(step['content'])

    def process_commands(self, cmds):
        """ Pretend to type the command, run it and then display the output """
        for cmd in cmds:
            self.type_command(cmd)
            results = self.executor.run_cmd(cmd)
            print(results, end="", flush=True)
        print()
        return results

    def type_command(self, cmd):
        """ Displays the command on the screen """

        # Must add ' ' when typing command because whitespaces are removed from configparser
        # https://docs.python.org/3/library/configparser.html#supported-ini-file-structure
        print(self.config.get('RENDER', 'CONSOLE_PROMPT', raw=True) + ' ', end="", flush=True)
        for _, char in enumerate(cmd):
            if char != "\n":
                typing_delay = None #float(self.config.get('RENDER', 'TYPING_DELAY'))
                if typing_delay:
                    delay = random.uniform(0.02, typing_delay)
                    time.sleep(delay)
                print(char, end="", flush=True)
        print("", flush=True)
