""" Automated mode for SimDem """

import logging
import difflib
from simdem.mode.common import ModeCommon

class AutomatedMode(ModeCommon):
    """ This class is the automated SimDem mode
        Does not display the descriptive text, but pauses at each
        code block. When the user hits a key the command is "typed", a
        second keypress executes the command.
    """

    def process_file(self, file_path):
        """ Parses the file and starts processing it """
        #print("*** Processing " + file_path + " ***")
        steps = self.parser.parse_file(file_path)

        last_command_result = None

        if 'prerequisites' in steps:
            for prereq_file in steps['prerequisites']:
                self.process_file(prereq_file)
        if 'validation_command' in steps:
            last_command_result = self.process_commands(steps['validation_command'])
        if 'validation_result' in steps:
            if not self.is_result_valid(steps['validation_result'], last_command_result):
                return

        """ I'd like to use a dispatcher for this; however, we need to exit processing
            if the validation fails. """
        for step in steps['body']:
            if step['type'] == 'commands':
                last_command_result = self.process_commands(step)
            elif step['type'] == 'result':
                self.is_result_valid(step['content'], last_command_result)


    def process_commands(self, step):
        """ Pretend to type the command, run it and then display the output """
        for cmd in step['content']:
            print(cmd, end="", flush=True)
            results = self.executor.run_cmd(cmd)
            print(results, end="", flush=True)
        print()
        return results

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
            print('***VALIDATION PASSED***')

        else:
            logging.error("is_result_valid failed")
            logging.error("actual_results = " + actual_results)
            logging.error("expected_results = " + expected_results)
            print('***VALIDATION FAILED***')

        return is_pass
