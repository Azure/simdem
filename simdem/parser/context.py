import logging
import pprint
import re

import mistletoe.ast_renderer as renderer
import mistletoe.block_token as token


class ContextParser(object):

    def is_command_block(self, block):
        if block['type'] == 'BlockCode' and block['language'] == 'shell':
            return True
        return False
    
    def is_result_block(self, block):
        #  This is different than previous SimDem because it didn't require a language for the result.
        #  I believe this approach is more declarative.
        if block['type'] == 'BlockCode' and block['language'] == 'result':
            return True
        return False

    """
    I'm not a fan of denoting prerequisites by using a header title, but that will suffice for now
    Will look like this coming out of AST
    {'children': [{'children': [{'content': 'Prerequisites', 'type': 'RawText'}],
               'level': 1,
               'type': 'Heading'},
    """
    def is_prerequisite_block(self, block):
        if 'children' in block and len(block['children']) and 'content' in block['children'][0] \
            and 'prerequisite' in block['children'][0]['content'].lower() and block['type'].lower() == 'heading':
            return True
        return False

    def parse_file(self, file_path):
        with open(file_path, 'r') as fin:
            ast = renderer.get_ast(token.Document(fin))
        
        res = {
            'prerequisites': [],
            'commands': []
        }

        idx = 0
        blocks = ast['children']
        #logging.debug("parse_file():processing " + str(blocks)
        while idx < len(blocks):
            block = blocks[idx]
            logging.debug("parse_file():processing " + str(block))
            
            if self.is_prerequisite_block(block):
                logging.debug("parse_file():found preqreq block")
                res['prerequisites'] = [x['children'][0]['target'] for x in blocks[idx+1]['children']]
                #  No need to process the next block since that's the prereqs
                idx = idx + 1

            elif self.is_result_block(block):
                # Assume that the result block is for the previous command block
                logging.debug("parse_file():is_result_block")
                content = block['children'][0]['content'].rstrip()
                if content:
                    res['commands'][len(res['commands']) - 1]['expected_result'] = content

            elif self.is_command_block(block):
                logging.debug("parse_file():is_command_block")
                for line in block['children'][0]['content'].split("\n"):
                    if line: 
                        res['commands'].append({ 'command': line })

            else:
                logging.info("get_commands():unknown_block.  Ignoring")

            idx = idx + 1
            #logging.debug(res)
        return res
