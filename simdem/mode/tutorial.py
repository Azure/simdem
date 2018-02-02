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

        # This breaks testcases right now.  Blarg
        # https://www.quora.com/Is-there-a-Clear-screen-function-in-Python
        #print("\033[H\033[J")
        #os.system('clear')
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
                        print('*** SIMDEM RESULT PASSED ***')
                    else:
                        print('*** SIMDEM RESULT FAILED ***')


    @staticmethod
    def process_heading(step):
        """ Print out the heading exactly as we found it """
        print(step['level'] * '#' + ' ' + step['content'])
        print()

    @staticmethod
    def process_text(step):
        """ Print out the text exactly as we found it """
        print(step['content'])
