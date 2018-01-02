""" This module hosts the CodeBlockParser
"""

from collections import defaultdict

from mistletoe import Document
from mistletoe.base_renderer import BaseRenderer

# Inspired by: https://gist.github.com/miyuchina/a06bd90d91b70be0906266760547da62

class CodeBlockParser(BaseRenderer):
    """ This class parses Markdown documents into SimDem Execution Objects
        This class expects all SimDem primitives to be parsed from code blocks,
        and uses the code block language to know which type of execution it is
    """
    def __init__(self):
        super().__init__()
        self.output = defaultdict(list)

    def render_block_code(self, token):
        """ Implemented as part of Mistletoe interface
            Given this object parses only code blocks, this is
            the only one with relevant logic.  The code block language
            is parsed to determine what type of object the code underneath is
        """
        lines = token.children[0].content.splitlines()
        if 'prerequisite' in token.language:
            self.output['prerequisites'].extend(lines)
        elif 'result' in token.language:
            self.output['commands'][-1]['expected_result'] = lines[0]
        elif 'shell' in token.language:
            self.output['commands'].extend({'command': line} for line in lines)
        else:
            logging.info("get_commands():unknown_block.  Ignoring")
        return ''

    def render_document(self, token):
        """ Implemented as part of the Mistletoe interface
        """
        self.render_inner(token)
        return dict(self.output)

    def __getattr__(self, name):
        """ Implemented as part of the Mistletoe interface
            Added to prevent Mistletoe from throwing warnings for missing render functions
        """
        return lambda token: ''

    def parse_file(self, file_path):
        """ Implemented as part of SimDem interface
            Renders the contents of the file path using this object as a Mistletoe renderer
        """
        with open(file_path, 'r') as fin:
            with CodeBlockParser() as renderer:
                rendered = renderer.render(Document(fin))
        return rendered
