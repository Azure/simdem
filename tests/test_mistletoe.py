# -*- coding: utf-8 -*-

from .context import simdem_renderer

import mistletoe
import unittest

import mistletoe.block_token as token
from mistletoe.ast_renderer import ASTRenderer
import mistletoe.ast_renderer as renderer



class SimDemMistletoeTestSuite(unittest.TestCase):
    """Lexer test cases."""

    def test_basic(self):
        doc = 'Nothing special here.  Move along'
        res = mistletoe.markdown(doc, simdem_renderer.SimdemRenderer)
        exp_res = [{'type': 'paragraph', 'text': 'Nothing special here.  Move along'}]
        self.assertEquals(res, exp_res)


    def test_strong(self):
        doc = 'This is **strong text**'
        res = mistletoe.markdown(doc, simdem_renderer.SimdemRenderer)
        exp_res = [{'type': 'paragraph', 'text': 'This is strong text'}]
        self.assertEquals(res, exp_res)

    '''
    def test_block_code(self):
        doc = ("```php", "echo $foo", 'echo bar', "```")
        print(doc)
        #res = mistletoe.markdown(doc, simdem_renderer.SimdemRenderer)
        res = mistletoe.markdown(doc, simdem_renderer.SimdemRenderer)
        exp_res = [{'lang': 'php', 'text': 'echo $foo', 'type': 'code'}]
        self.assertEquals(res, exp_res)
    '''

    def test_block_code_file(self):
        file_path = '/tmp/foo4.md'
        with open(file_path, 'r') as fin:
            res = mistletoe.markdown(fin, simdem_renderer.SimdemRenderer)
        exp_res = [{'lang': 'php', 'text': ['echo $foo', 'echo $bar'], 'type': 'code'}]
        self.assertEquals(res, exp_res)
    '''
    def test_ast(self):
        self.maxDiff = None
        file_path = 'content/simple/README.md'
        file_path = '/tmp/foo3.md'
        with open(file_path, 'r') as fin:
            res = renderer.get_ast(token.Document(fin))

        self.assertEqual(res, {})
    '''

#        with open('content/simple/README.md', 'r') as fin:
#            output = renderer.get_ast(fin)



if __name__ == '__main__':
    unittest.main()
