""" Common mode for SimDem mode """

import os
import logging
import difflib

class ModeCommon(object): # pylint: disable=R0903
    """ This class is designed to hold any shared code across modes
    """
    config = None
    executor = None
    parser = None

    def __init__(self, config, parser, executor):
        self.config = config
        self.parser = parser
        self.executor = executor

    def process_file(self, file_path, is_prereq=False):
        """ Parses the file and starts processing it """
        logging.debug("parse_file(file_path=" + file_path + ", is_prereq=" + str(is_prereq))
        # Change the working directory in case of any recursion
        start_path = os.path.dirname(file_path)
        steps = self.parser.parse_file(file_path)

        #  Begin preqreq processing
        if 'prerequisites' in steps:
            for prereq_file in steps['prerequisites']:
                # Change the working directory in case of any recursion
                self.process_file(start_path + '/' + prereq_file, is_prereq=True)
        if is_prereq and 'validation' in steps:
            last_command_result = self.process_commands(steps['validation']['commands']) # pylint: disable=no-member
            if 'expected_result' in steps['validation']:
                if self.is_result_valid(steps['validation']['expected_result'],
                                        last_command_result):
                    #print('***PREREQUISITE VALIDATION PASSED***')
                    return
                else:
                    print('***PREREQUISITE VALIDATION FAILED***')
        #  End prereq processing

        self.executor.run_cmd('cd ' + start_path)
        self.process(steps) # pylint: disable=no-member

        if 'next_steps' in steps:
            self.process_next_steps(steps['next_steps'], start_path) # pylint: disable=no-member

    def process_commands(self, cmds):
        """ Pretend to type the command, run it and then display the output """
        for cmd in cmds:
            print(self.config.get('render', 'console_prompt', raw=True) + ' ' + cmd)
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

        else:
            logging.error("is_result_valid failed")
            logging.error("actual_results = " + actual_results)
            logging.error("expected_results = " + expected_results)

        return is_pass
