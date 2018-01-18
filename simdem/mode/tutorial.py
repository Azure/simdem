""" Tutorial mode for SimDem"""

import logging
from simdem.mode.common import ModeCommon

class TutorialMode(ModeCommon):
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
        print()

    @staticmethod
    def process_next_steps(steps):
        """ Is there a good way to test this that doesn't involve lots of test code + expect?
            Not fully tested yet.  Low priority feature.
        """
        idx = 1
        if steps:
            print("Next steps available:")
            for step in steps:
                print(idx + ".) " + step['title'])
                idx += 1
            step_request = input("Which step do you want to take next?")
            if step_request:
                return steps[step_request+1]['target']
        return
