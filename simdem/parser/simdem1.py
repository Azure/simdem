""" This module hosts the ContextParser
"""

import logging

import mistletoe.ast_renderer as renderer
import mistletoe.block_token


class SimDem1Parser(object):
    """ This class parses the human readable markdown using a defined syntax to
        know how to create the SimDem Execution Object
        and uses the code block language to know which type of execution it is
    """

    mode = None

    def set_mode(self, mode):
        logging.debug('set_mode(' + str(mode) + ')')
        self.mode = mode

    def parse_file(self, file_path):
        """ The main meat for parsing the file.  Uses mistletoe's AST parser
            to create a tokenized object and then parses that tokenized object
            into SimDem Execution Object
        """
        with open(file_path, 'r') as fin:
            ast = renderer.get_ast(mistletoe.block_token.Document(fin))
        res = []

        for token in ast['children']:
            logging.debug("parse_file():processing " + str(token))

            # Heading
            if token['type'] == 'Heading':
                res.append({'type': 'heading', 'level': token['level'],
                            'content': token['children'][0]['content']})
                logging.debug("parse_file():found heading")

                # Prerequisite Heading
                if token['children'][0]['content'].lower() == 'prerequisites':
                    self.set_mode('prerequisites')

                # Next Steps Heading
                elif token['children'][0]['content'].lower() == 'next steps':
                    self.set_mode('next_steps')

                # Results Heading
                elif token['children'][0]['content'].lower() == 'result':
                    self.set_mode('result')

                # Validation Heading
                elif token['children'][0]['content'].lower() == 'validation':
                    self.set_mode('validation')

                else:
                    logging.debug("parse_file():unable to determing header type.")
                    self.set_mode(None)

            # Prerequisite List
            elif token['type'] == 'List' and self.mode == 'prerequisites':
                logging.debug("parse_file():found prerequisites list")
                titles = [x['children'][0]['children'][0]['content'] for x in token['children']]
                content_t = "\n".join(' * ' + x for x in titles)
                # Make sure to print out the page contents too
                res.append({'type': 'text', 'content': content_t})
                
                content_p = [x['children'][0]['target'] for x in token['children']]
                res.append({'type': 'prerequisites', 'content': content_p})

            # Paragraph
            elif token['type'] == 'Paragraph':
                logging.debug("parse_file():found paragraph")
                if token['children']:
                    content = token['children'][0]['content']
                    # Result Paragraph
                    if content == 'Results:':
                        if self.mode == 'validation':
                            self.set_mode('validation_result')
                        else:
                            self.set_mode('result')
                        #res.append({'type': 'result', 'content': content})
                    # Regular Paragraph
                    else:
                        res.append({'type': 'text', 'content': content})

            elif token['type'] == 'BlockCode':
                # Result Block Code
                if self.mode == 'validation':
                    logging.debug("parse_file():found validation block code")
                    content = [line for line in token['children'][0]['content'].split("\n") if line]
                    res.append({'type': 'validation_command', 'content': content})

                # Validation Result Block Code
                elif self.mode == 'validation_result':
                    logging.debug("parse_file():found validation result block code")
                    content = token['children'][0]['content'].rstrip()
                    res.append({'type': 'validation_result', 'content': content})

                # Result Block Code
                elif self.mode == 'result':
                    logging.debug("parse_file():found result block code")
                    content = token['children'][0]['content'].rstrip()
                    res.append({'type': 'result', 'content': content})

                # Block Code (regular)
                elif self.mode is None:
                    logging.debug("parse_file():found block code")
                    content = [line for line in token['children'][0]['content'].split("\n") if line]
                    res.append({'type': 'commands', 'content': content})

                else:
                    logging.debug('parse_file():unexpected Block Code mode (' + self.mode + ')')

            else:
                logging.debug('parse_file():unknown token type (type=' + token['type'] + 
                              ';mode=' + self.mode + ').  Igorning')

        return res
