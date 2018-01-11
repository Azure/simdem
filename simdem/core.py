# -*- coding: utf-8 -*-
"""Contains only core SimDem object"""

import difflib
import logging

class Core(object):
    """The core glue for SimDem is here.  It uses dependency injection so that the
       implementation of the renderer, parser and executor are left to the classes passed in.
    """

    renderer = None
    config = None
    parser = None
    executor = None

    def __init__(self, config, renderer, parser, executor):
        self.config = config
        self.renderer = renderer
        self.parser = parser
        self.executor = executor

    def run_code_block(self, cmd_block):
        """In the future, we'll want to split a code segment into individual lines
           For now, assume just one command in a block
           Returning the latest result so we can validate the result.
           We might want to validate the result of the entire block, but for now,
           validate just the last run command
        """
        result_latest = None
        for cmd in cmd_block.split("\n"):
            result_latest = self.run_cmd(cmd)
        return result_latest

    def run_cmd(self, cmd):
        """ prints out the command, runs it and then displays the results """
        self.renderer.type_command(cmd)
        res = self.executor.run_cmd(cmd)
        self.renderer.display_result(res)
        return res

    def process_file(self, file_path):
        """ Parses the file and then runs any prerequisites """
        blocks = self.parser.parse_file(file_path)
        logging.info("process_file():blocks=" + str(blocks))
        if 'prerequisites' in blocks:
            self.process_prereqs(blocks['prerequisites'])
            logging.info("process_file():completed process_prereqs()")
        result = self.run_command_blocks(blocks['commands'])
        return result

    def process_prereqs(self, prereqs):
        """ Loops through each of the prerequisites """
        logging.info("process_preqreqs():" + str(prereqs))
        for prereq_file in prereqs:
            self.process_file(prereq_file)

    def run_command_blocks(self, commands):
        """ For each block, run and validate the output """
        logging.info("run_command_blocks():blocks=" + str(commands))
        for command in commands:
            logging.info("run_command_blocks():processing " + str(command))
            result = self.run_code_block(command['command'])
            if 'expected_result' in command:
                if self.is_result_valid(command['expected_result'], result):
                    logging.info("Result passed")
                else:
                    logging.error("Result did not pass")
                    return

    def show_next_steps(self, steps):
        """ If there's any next steps to take, let the renderer process them """
        logging.info("run_blocks():steps=" + str(steps))
        step_request_target = self.renderer.get_next_step(steps)
        if step_request_target:
            self.process_file(step_request_target)

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
