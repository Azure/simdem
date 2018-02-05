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

        self.ui.clear()
        for step in steps['body']:
            if step['type'] == 'heading':
                self.process_heading(step)
            elif step['type'] == 'text':
                self.process_text(step)
            elif step['type'] == 'commands':
                last_command_result = self.process_commands(step['content'])
                logging.debug(step)
                if 'expected_result' in step:
                    if self.is_result_valid(step['expected_result'], last_command_result):
                        self.ui.print_test_passed()
                    else:
                        self.ui.print_test_failed()


    def process_heading(self, step):
        """ Print out the heading exactly as we found it """
        self.ui.println(step['level'] * '#' + ' ' + step['content'])
        self.ui.println()

    def process_text(self, step):
        """ Print out the text exactly as we found it """
        self.ui.println(step['content'])
