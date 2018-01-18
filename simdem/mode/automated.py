""" Automated mode for SimDem """

import logging
from simdem.mode.common import ModeCommon

class AutomatedMode(ModeCommon):
    """ This class is the automated SimDem mode
        Does not display the descriptive text, but pauses at each
        code block. When the user hits a key the command is "typed", a
        second keypress executes the command.
    """

    def process(self, steps):
        """ I'd like to use a dispatcher for this; however, we need to exit processing
            if the validation fails. """
        logging.debug("process()")
        for step in steps['body']:
            if step['type'] == 'commands':
                last_command_result = self.process_commands(step['content'])
                if 'expected_results' in step:
                    if self.is_result_valid(step['content'], last_command_result):
                        print('***VALIDATION FAILED***')
                    else:
                        print('***VALIDATION PASSED***')
