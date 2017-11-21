# -*- coding: utf-8 -*-
from . import helpers,executor
import mistune

def start():
    exe = executor.Executor()
    sh = exe.get_shell()

def run_code_block(cmd):
    # In the future, we'll want to split a code segment into individual lines
    # For now, assume just one command in a block
    return run_cmd(cmd)

def run_cmd(cmd):
    exe = executor.Executor()
    return exe.run_cmd(cmd)

def parse_doc(text):
    blockLexer = mistune.BlockLexer()
    return blockLexer.parse(text)

def run_doc(text):
    blocks = parse_doc(text)
    for block in blocks:
        print(block)
        if block['type'] == 'code' and block['lang'] == 'shell':
            run_code_block(block['text'])