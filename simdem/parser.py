import re
import logging

class Parser(object):

    lexer = None

    def __init__(self, lexer):
        self.lexer = lexer

    def is_prerequisite_block(self, block):
        # Example: {'level': 1, 'text': 'Prerequisites', 'type': 'heading'}
        if 'prerequisite' in block['text'].lower() and block['type'] == 'heading':
            return True
        return False

    def is_command_block(self, block):
        if block['type'] == 'code' and block['lang'] == 'shell':
            return True
        return False
    
    def is_result_block(self, block, block_prev):
        if block['type'] == 'code' and block['lang'] == 'shell' and \
            block_prev['type'] == 'paragraph' and block_prev['text'].lower().startswith('results:'):
            return True
        return False

    # Assuming just one for now
    def parse_ref_from_text(self, text):
        # Does mistune allow us to parse this?  Would be nice.
        pattern = re.compile('.*\[(.*)\]\((.*)\).*')
        match = pattern.match(text)
        if match:
            title = match.groups()[0].strip()
            href = match.groups()[1]
            logging.debug("Found prereq: " + href)
            return href
        return None

    def get_prereqs(self, blocks):
#        logging.debug("get_prereqs: " + str(blocks))
        res = []
        #  Is there a better way to do this?  Probably so.  I'm on a plane and can't research
        for idx in range(len(blocks)):
            block = blocks[idx]
            if self.is_prerequisite_block(block):
                # We want the text block after the prereq heading
                for line in blocks[idx+1]['text'].split("\n"):
                    res.append(line)
#        logging.debug("get_prereqs: res= " + str(res))
        return res


    def get_file_contents(self, file_path):
#        logging.debug("get_file_contents: " + file_path)
        f = open(file_path, 'r')
        content = f.read()
        f.close()
        return content

    def parse_doc2(self, text):
#        logging.debug("parse_doc: text=" + text)
        # https://github.com/lepture/mistune/issues/147
        # Stoopid non-idempotent parser.
        self.lexer.tokens = []
        blocks = self.lexer.parse(text)
        return {
            'prerequisites': self.get_prereqs(blocks),
            'commands': self.get_commands(blocks)
        }

    def get_commands(self, blocks):
        res = []
        for idx in range(len(blocks)):
            logging.debug("get_commands():processing " + str(blocks[idx]))
            block = blocks[idx]
            block_prev = blocks[idx-1]
            if self.is_result_block(block, block_prev):
                logging.debug("get_commands():is_result_block")
            elif self.is_command_block(block):
                logging.debug("get_commands():is_command_block")
                for line in block['text'].split("\n"):
                    res.append(line)
            else:
                logging.debug("get_commands():unknown_block")
        return res

    def parse_doc(self, text):
#        logging.debug("parse_doc: text=" + text)
        # https://github.com/lepture/mistune/issues/147
        # Stoopid non-idempotent parser.
        self.lexer.tokens = []
        res = self.lexer.parse(text)

        logging.debug("parse_doc: res=" + str(res))
        return res
