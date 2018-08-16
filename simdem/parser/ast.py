""" This module hosts the ContextParser
"""

import mistletoe.ast_renderer as renderer
import mistletoe.block_token


class AstParser(object): # pylint: disable=R0903
    """ This class parses the human readable markdown using a defined syntax to
        know how to create the SimDem Execution Object
        and uses the code block language to know which type of execution it is
    """

    @staticmethod
    def parse_file(file_path):
        """ The main meat for parsing the file.  Uses mistletoe's AST parser
            to create a tokenized object and then parses that tokenized object
            into SimDem Execution Object
        """
        with open(file_path, 'r') as fin:
            ast = renderer.get_ast(mistletoe.block_token.Document(fin))
        return ast
