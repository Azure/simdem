# -*- coding: utf-8 -*-
from . import executor
import difflib
import logging

class Core(object):

    rend = None
    lexer = None
    config = None

    def __init__(self, config, rend, lexer):
        self.config = config
        self.rend = rend
        self.lexer = lexer

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
        content = self.get_file_contents(file_path)
        result = self.run_doc(content)
        return result

    def get_file_contents(self, file_path):
        f = open(file_path, 'r')
        try:
            content = f.read()
        finally:
            f.close()
        return content

    def parse_doc(self, text):
        return self.lexer.parse(text)

    def run_doc(self, text):
        blocks = self.parse_doc(text)
        results_latest = None
        for idx in range(len(blocks)):
            if self.is_result_block(blocks, idx):
                is_passable = self.is_result_passable(blocks[idx]['text'], results_latest)
                if not is_passable:
                    logging.error("Result did not pass")
                    return
            elif self.is_runable_block(blocks[idx]):
                results_latest = self.run_code_block(blocks[idx]['text'])
   
    def is_runable_block(self, block):
        if block['type'] == 'code' and block['lang'] == 'shell':
            return True
        return False
    
    def is_result_block(self, blocks, idx):
        block = blocks[idx]
        block_prev = blocks[idx-1]
        if block['type'] == 'code' and block['lang'] == 'shell' and \
            block_prev['type'] == 'paragraph' and block_prev['text'].lower().startswith('results:'):
            return True
        return False


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