""" Automated mode for SimDem """

import logging
from simdem.mode.common import ModeCommon

class AutomatedMode(ModeCommon):
    """ This class is the automated SimDem mode
        Does not display the descriptive text, but pauses at each
        code block. When the user hits a key the command is "typed", a
        second keypress executes the command.
    """

    def process_file(self, file_path, is_prereq=False):
        """ Parses the file and starts processing it """
        logging.debug("parse_file(file_path=" + file_path + ", is_prereq=" + str(is_prereq))
        steps = self.parser.parse_file(file_path)

        #  Begin prereq body
        if 'prerequisites' in steps:
            for prereq_file in steps['prerequisites']:
                self.process_file(prereq_file, is_prereq=True)
        if is_prereq and 'validation' in steps:
            last_command_result = self.process_commands(steps['validation']['commands'])
            if 'expected_result' in steps['validation']:
                if self.is_result_valid(steps['validation']['expected_result'],
                                        last_command_result):
                    print('***PREREQUISITE VALIDATION PASSED***')
                    return
                else:
                    print('***PREREQUISITE VALIDATION FAILED***')
        #  End prereq body

        """ I'd like to use a dispatcher for this; however, we need to exit processing
            if the validation fails. """
        for step in steps['body']:
            if step['type'] == 'commands':
                last_command_result = self.process_commands(step)
                if step['expected_result'] == 'result':
                    if self.is_result_valid(step['content'], last_command_result):
                        print('***VALIDATION FAILED***')
                    else:
                        print('***VALIDATION PASSED***')

    def process_commands(self, step):
        """ Pretend to type the command, run it and then display the output """
        for cmd in step['content']:
            print(cmd, end="", flush=True)
            results = self.executor.run_cmd(cmd)
            print(results, end="", flush=True)
        print()
        return results
