import re
import logging

class Parser(object):

    def is_prerequisite_block(self, block):
        # Example: {'level': 1, 'text': 'Prerequisites', 'type': 'heading'}
        if 'prerequisite' in block['text'].lower() and block['type'] == 'heading':
            return True
        return False

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

