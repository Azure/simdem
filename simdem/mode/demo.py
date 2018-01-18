"""Demo (default) mode for SimDem"""

import random
import time
import logging
from simdem.mode.common import ModeCommon

class DemoMode(ModeCommon):
    """ This class is the default SimDem file processor.
        It's designed for running files in a demo-able mode that looks like a human is typing it
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
