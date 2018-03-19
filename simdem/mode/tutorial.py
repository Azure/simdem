""" Tutorial mode for SimDem"""

import os
import sys
import logging
from simdem.mode.interactive import InteractiveMode

class TutorialMode(InteractiveMode):
    """ This class is the tutorial mode class for SimDem.
        It's designed for running files in a tutorial mode which Displays the descriptive text
        of the tutorial and pauses at code blocks to allow user interaction.
    """

    def process(self, steps):
        """ Processes the steps from a processed file """
        logging.debug("process()")

        last_text = None
#        self.ui.clear()
        for step in steps['body']:
            if step['type'] == 'heading':
                self.ui.print_heading(step['content'], step['level'])
            elif step['type'] == 'text':
                self.ui.println(step['content'])
                last_text = step['content']
            elif step['type'] == 'commands':
                last_command_result = self.process_commands(step['content'], last_text=last_text)
                logging.debug(step)
                if 'expected_result' in step:
                    if self.is_result_valid(step['expected_result'], last_command_result):
                        self.ui.print_test_passed()
                    else:
                        self.ui.print_test_failed()
