""" This module hosts the ContextParser
"""

import logging

import mistletoe.ast_renderer as renderer
import mistletoe.block_token as token


class ContextParser(object):
    """ This class parses the human readable markdown using a defined syntax to 
        know how to create the SimDem Execution Object
        and uses the code block language to know which type of execution it is
    """

    def is_command_block(self, block):
        """ Expects a code block with a shell command in it
        """
        if block['type'] == 'BlockCode' and block['language'] == 'shell':
            return True
        return False
    
    def is_result_block(self, block):
        #  This is different than previous SimDem because it didn't require a language for the result.
        #  I believe this approach is more declarative.
        if block['type'] == 'BlockCode' and block['language'] == 'result':
            return True
        return False

    def is_next_step_block(self, block):
        """ This block is similiar to "choose your own adventure" games 
            This feature allows you to determine which document you want to process after you complete the current one
        """
        if 'children' in block and len(block['children']) and 'content' in block['children'][0] \
            and 'next step' in block['children'][0]['content'].lower() and block['type'].lower() == 'heading':
            return True
        return False

    def is_prerequisite_block(self, block):
        """
        I'm not a fan of denoting prerequisites by using a header title, but that will suffice for now
        Will look like this coming out of AST
        {'children': [{'children': [{'content': 'Prerequisites', 'type': 'RawText'}],
                'level': 1,
                'type': 'Heading'},
        """
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

            elif self.is_next_step_block(block):
                logging.debug("parse_file():is_next_step_block")
                block = blocks[idx]
                # Fast-forward to find the list block inside this header block.
                # Maybe we should also test to verify we haven't gone past the header block?
                while 'List' not in block['type'] and idx < len(blocks):
                    idx = idx + 1
                    block = blocks[idx]
                print(block)
                res['next_steps'] = [{'target': x['target'], 'title': x['children'][0]['content']} for x in block['children'][0]['children'] if x['type'] == 'Link']

            else:
                logging.info("get_commands():unknown_block.  Ignoring")

            idx = idx + 1
            #logging.debug(res)
        return res
