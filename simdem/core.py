# -*- coding: utf-8 -*-
from . import helpers,executor

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
        for cmd in cmd_block.split("\n"):
            self.run_cmd(cmd)

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
        for block in blocks:
            if block['type'] == 'code' and block['lang'] == 'shell':
                self.run_code_block(block['text'])