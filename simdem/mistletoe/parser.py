import re
import logging
import mistletoe.ast_renderer as renderer
import mistletoe.block_token as token
import pprint

class MistletoeParser(object):

    def __init__(self):
        return

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

    def get_prereqs(self, doc):
        logging.debug("get_prereqs: ")
        pprint.pprint(doc)
        res = []
        #  Is there a better way to do this?  Probably so.  I'm on a plane and can't research
        for idx in range(len(doc['children'])):
            block = doc['children'][idx]
            logging.debug("get_prereqs():processing " + str(block))
            if self.is_prerequisite_block(block):
                logging.debug("get_prereqs():found preqreq block")
                res = [x['children'][0]['target'] for x in doc['children'][idx+1]['children']]
                logging.debug(res)
        return res


    def get_file_contents(self, file_path):
#        logging.debug("get_file_contents: " + file_path)
        f = open(file_path, 'r')
        content = f.read()
        f.close()
        return content

    def parse_file(self, file_path):
        with open(file_path, 'r') as fin:
            ast = renderer.get_ast(token.Document(fin))

        return {
            'prerequisites': self.get_prereqs(ast),
            'commands': self.get_commands(ast)
        }

    def get_commands(self, doc):
        res = []
        for idx in range(len(doc['children'])):
            logging.debug("get_commands():processing " + str(doc['children'][idx]))
            block = doc['children'][idx]
            if self.is_result_block(block):
                logging.debug("get_commands():is_result_block")
                res[len(res) - 1]['expected_result'] = block['children'][0]['content']
            elif self.is_command_block(block):
                logging.debug("get_commands():is_command_block")
                for line in block['children'][0]['content'].split("\n"):
                    if line: 
                        res.append({ 'command': line })
            else:
                logging.info("get_commands():unknown_block.  Ignoring")
        return res