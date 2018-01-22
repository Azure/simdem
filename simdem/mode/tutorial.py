""" Tutorial mode for SimDem"""

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

        for step in steps['body']:
            if step['type'] == 'heading':
                self.process_heading(step)
            elif step['type'] == 'text':
                self.process_text(step)
            elif step['type'] == 'commands':
                self.process_commands(step['content'])


    @staticmethod
    def process_heading(step):
        """ Print out the heading exactly as we found it """
        print(step['level'] * '#' + ' ' + step['content'])
        print()

    @staticmethod
    def process_text(step):
        """ Print out the text exactly as we found it """
        print(step['content'])
