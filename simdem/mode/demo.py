"""Demo (default) mode for SimDem"""

import random
import time
import logging
from simdem.mode.interactive import InteractiveMode

class DemoMode(InteractiveMode):
    """ This class is the default SimDem file processor.
        It's designed for running files in a demo-able mode that looks like a human is typing it
    """

    def process(self, steps):
        """ Processes the steps from a processed file """
        logging.debug("process()")

        for step in steps['body']:
            if step['type'] == 'commands':
                self.process_commands(step['content'])

    def display_command(self, cmd):
        """ Displays the command on the screen """

        # Must add ' ' when typing command because whitespaces are removed from configparser
        # https://docs.python.org/3/library/configparser.html#supported-ini-file-structure
        for _, char in enumerate(cmd):
            if char != "\n":
                typing_delay = float(self.config.get('render', 'typing_delay'))
                if typing_delay:
                    delay = random.uniform(0.02, typing_delay)
                    time.sleep(delay)
                self.ui.print(char)
        self.ui.print_break()
