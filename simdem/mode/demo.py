"""Demo (default) renderer for SimDem"""

import random
import time
import logging
import difflib

class DemoMode(object):
    """ This class is used to render the output of the commands into something
        that looks like you're typing
    """
    config = None
    executor = None
    parser = None

    def __init__(self, config, executor, parser):
        self.config = config
        self.executor = executor
        self.parser = parser

    def process_file(self, file_path):
        print("*** Processing " + file_path + " ***")
        steps = self.parser.parse_file(file_path)
        self.process(steps)
        print("*** Completed Processing " + file_path + " ***")

    def process(self, steps):
        last_command_result = None

        for step in steps:
            if step['type'] == 'heading':
                self.process_heading(step)
            elif step['type'] == 'text':
                self.process_text(step)
            elif step['type'] == 'commands':
                last_command_result = self.process_commands(step)
            elif step['type'] == 'result':
                if self.is_result_valid(step['content'], last_command_result):
                    print('***VALIDATION PASSED***')
                else:
                    print('***VALIDATION FAILED***')
            elif step['type'] == 'prerequisites':
                for prereq_file in step['content']:
                    self.process_file(prereq_file)
            elif step['type'] == 'validation_command':
                last_command_result = self.process_commands(step)
            elif step['type'] == 'validation_result':
                if self.is_result_valid(step['content'], last_command_result):
                    print('***VALIDATION PASSED***')
                    return
                else:
                    print('***VALIDATION FAILED***')


    def process_heading(self, step):
        print(step['level'] * '#' + ' ' + step['content'])
        print()

    def process_text(self, step):
        print(step['content'])
        print()

    def process_commands(self, step):
        for cmd in step['content']:
            self.type_command(cmd)
            results = self.executor.run_cmd(cmd)
            self.display_result(results)
        print()
        return results

    def process_result(self, ):
        print('***CHECKING RESULT***')
        print('RES= ' + step['content'])
        print()

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

    @staticmethod
    def display_result(res):
        """Demo specific implementation of displaying to the screen"""
        print(res, end="", flush=True)

    @staticmethod
    def is_result_valid(expected_results, actual_results, expected_similarity=1.0):
        """Checks to see if a command execution passes.
        If actual results compared to expected results is within
        the expected similarity level then it's considered a pass.

        expected_similarity = 1.0 could be a breaking change for older SimDem scripts.
        explicit fails > implicit passes
        Ross may disagree with me.  Let's see how this story unfolds.
        """

        if not actual_results:
            logging.error("is_result_valid(): actual_results is empty.")
            return False

        logging.debug("is_result_valid(" + expected_results + "," + actual_results + \
            "," + str(expected_similarity) + ")")

        expected_results_str = expected_results.rstrip()
        actual_results_str = actual_results.rstrip()
        logging.debug("is_result_valid(" + expected_results_str + "," + actual_results_str + \
            "," + str(expected_similarity) + ")")
        seq = difflib.SequenceMatcher(lambda x: x in " \t\n\r",
                                      actual_results_str,
                                      expected_results_str)

        is_pass = seq.ratio() >= expected_similarity

        if is_pass:
            logging.info("is_result_valid passed")
        else:
            logging.error("is_result_valid failed")
            logging.error("actual_results = " + actual_results)
            logging.error("expected_results = " + expected_results)

        return is_pass
