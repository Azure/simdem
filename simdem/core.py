# -*- coding: utf-8 -*-
from . import executor,parser
import difflib
import logging
import re

class Core(object):

    rend = None
    config = None
    parser = None

    def __init__(self, config, rend, parser):
        self.config = config
        self.rend = rend
        self.parser = parser

    def run_code_block(self, cmd_block):
        # In the future, we'll want to split a code segment into individual lines
        # For now, assume just one command in a block
        # Returning the latest result so we can validate the result.
        # We might want to validate the result of the entire block, but for now, validate just the last run command
        result_latest = None
        for cmd in cmd_block.split("\n"):
            result_latest = self.run_cmd(cmd)
        return result_latest

    def run_cmd(self, cmd):
        return self.rend.run_cmd(cmd)

    def process_file(self, file_path):
        logging.info("process_file():file_path=" + file_path)
        content = self.parser.get_file_contents(file_path)
        logging.info("process_file():content=" + str(content))
        blocks = self.parser.parse_doc(content)
        logging.info("process_file():blocks=" + str(blocks))
        self.process_prereqs(blocks)
        logging.info("process_file():completed process_prereqs()")
        result = self.run_blocks(blocks)
        return result

    def process_prereqs(self, blocks):
        prereqs = self.parser.get_prereqs(blocks)
        logging.info("process_preqreqs():" + str(prereqs))
        for prereq_file in prereqs:
#            prereq_content = self.parser.get_file_contents(prereq_file)
#            preqreq_blocks = self.parser.parse_doc(prereq_content)
#            preqreq_validation = self.parser.get_validation_block(preqreq_blocks)
#            if not self.is_prereq_required(preqreq_validation):
            self.process_file(prereq_file)

    def run_blocks(self, blocks):
        logging.info("run_blocks():blocks=" + str(blocks))
        results_latest = None
        for idx in range(len(blocks)):
            logging.info("run_blocks():processing " + str(blocks[idx]))
            if self.parser.is_result_block(blocks, idx):
                logging.info("run_blocks():is_result_block")
                is_passable = self.is_result_passable(blocks[idx]['text'], results_latest)
                if not is_passable:
                    logging.error("Result did not pass")
                    return
            elif self.parser.is_runable_block(blocks[idx]):
                logging.info("run_blocks():is_runable_block")
                results_latest = self.run_code_block(blocks[idx]['text'])

    
    def is_result_passable(self, expected_results, actual_results, expected_similarity = 1.0):
        """Checks to see if a command execution passes.
        If actual results compared to expected results is within
        the expected similarity level then it's considered a pass.

        expected_similarity = 1.0 could be a breaking change for older SimDem scripts.
        explicit fails > implicit passes
        Ross may disagree with me.  Let's see how this story unfolds.
        """

        if not actual_results:
            logging.error("is_result_passable(): actual_results is empty.")
            return False

        logging.debug("is_result_passable(" + expected_results + "," + actual_results + "," + str(expected_similarity) + ")")

        expected_results_str = expected_results.rstrip()
        actual_results_str = actual_results.rstrip()
        logging.debug("is_result_passable(" + expected_results_str + "," + actual_results_str + "," + str(expected_similarity) + ")")
        seq = difflib.SequenceMatcher(lambda x: x in " \t\n\r", actual_results_str, expected_results_str)

        is_pass = seq.ratio() >= expected_similarity

        if is_pass:
            logging.info("is_result_passable passed")
        else:
            logging.error("is_result_passable failed")
            logging.error("actual_results = " + actual_results)
            logging.error("expected_results = " + expected_results)

        return is_pass 