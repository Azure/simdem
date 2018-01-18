""" Tutorial mode for SimDem"""

import logging
from simdem.mode.common import ModeCommon

class TutorialMode(ModeCommon):
    """ This class is the tutorial mode class for SimDem.
        It's designed for running files in a tutorial mode which Displays the descriptive text
        of the tutorial and pauses at code blocks to allow user interaction.
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

    def process_commands(self, cmds):
        """ Pretend to type the command, run it and then display the output """
        for cmd in cmds:
            print(self.config.get('RENDER', 'CONSOLE_PROMPT', raw=True) + ' ' + cmd)
            results = self.executor.run_cmd(cmd)
            print(results, end="", flush=True)
        print()
        return results

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
