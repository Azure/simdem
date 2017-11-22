# -*- coding: utf-8 -*-
from . import helpers,executor
import mistune
from .render import demo

class Core(object):

    def start(self):
        exe = executor.Executor()
        sh = exe.get_shell()

    def run_code_block(self, cmd):
        # In the future, we'll want to split a code segment into individual lines
        # For now, assume just one command in a block
        return self.run_cmd(cmd)

    def run_cmd(self, cmd):
        rend = demo.Demo()
        return rend.run_cmd(cmd)

    def parse_doc(self, text):
        blockLexer = mistune.BlockLexer()
        return blockLexer.parse(text)

    def run_doc(self, text):
        blocks = self.parse_doc(text)
        for block in blocks:
            print(block)
            if block['type'] == 'code' and block['lang'] == 'shell':
                self.run_code_block(block['text'])