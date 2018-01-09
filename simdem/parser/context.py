""" This module hosts the ContextParser
"""

import logging    # XXX: implement proper logging

from mistletoe.block_token import BlockToken, Document, tokenize
from mistletoe.base_renderer import BaseRenderer

class Section(BlockToken):
    def __init__(self, lines):
        self.heading = lines[0].strip().split('# ')[1].lower()
        # self.children contains other block tokens in this section
        super().__init__(lines[1:], tokenize)

    @staticmethod
    def start(line):
        return line.startswith('#')

    @staticmethod
    def read(lines):
        """Read until before the next heading."""
        line_buffer = []
        while lines.peek() is not None and not lines.peek().startswith('#'):
            line_buffer.append(next(lines))
        return line_buffer


class ContextParser(BaseRenderer):
    def __init__(self):
        self.res = {
            'prerequisites': [],
            'commands': []
        }
        self._in_prereq = False
        self._in_next_steps = False
        # add Section to the tokenizing process
        super().__init__(Section)

    def render_section(self, token):
        if 'prerequisites' in token.heading.lower(): # prereq section
            self._in_prereq = True
        elif 'next steps' in token.heading.lower():  # next steps section
            self._in_next_steps = True
        rendered = self.render_inner(token)
        self._in_prereq = False
        self._in_next_steps = False
        return rendered

    def render_link(self, token):
        rendered = self.render_inner(token)
        if self._in_prereq:
            self.res['prerequisites'].append(token.target)
        elif self._in_next_steps:
            step = {'title': rendered, 'target': token.target}
            try:
                self.res['next_steps'].append(step)
            except KeyError:
                self.res['next_steps'] = [step]
        return rendered

    def render_block_code(self, token):
        if token.language == 'shell':     # commands
            lines = token.children[0].content.splitlines()
            self.res['commands'].extend({'command': line} for line in lines)
        elif token.language == 'result':  # expected result
            line = token.children[0].content.strip()
            self.res['commands'][-1]['expected_result'] = line
        return self.render_inner(token)

    def render_raw_text(self, token):
        return token.content

    def __getattr__(self, name):
        """
        All other render functions returns the result of render_inner.
        """
        if name.startswith("render"):
            return self.render_inner
        # if not accessing a render function, raise AttributeError
        error_msg = "'{}' object has no attribute '{}'".format(self.__class__.__name__, name)
        raise AttributeError(error_msg)

    def parse_file(self, file_path):
        with open(file_path, 'r') as fin:
            self.render(Document(fin))
        return self.res

