from mistletoe.base_renderer import BaseRenderer
from mistletoe import Document
from collections import defaultdict
import logging

# Inspired by: https://gist.github.com/miyuchina/a06bd90d91b70be0906266760547da62

class SimdemMistletoeRenderer(BaseRenderer):
    def __init__(self):
        super().__init__()
        self.output = defaultdict(list)

    def render_block_code(self, token):
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
        self.render_inner(token)
        return dict(self.output)

    def __getattr__(self, name):
        return lambda token: ''

    def render_file(self, file_path):
        with open(file_path, 'r') as fin:
            with SimdemMistletoeRenderer() as renderer:
                rendered = renderer.render(Document(fin))
        return rendered