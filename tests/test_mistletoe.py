# -*- coding: utf-8 -*-
"""SimDem Test Case"""

import unittest

import mistletoe.ast_renderer as renderer
import mistletoe.block_token as token


class SimDemMistletoeTestSuite(unittest.TestCase):
    """Lexer test cases."""

    def test_ast(self):
        """Verify we understand how the Mistletoe AST parsers work"""
        #self.maxDiff = None

        file_path = 'content/simple/README.md'
        with open(file_path, 'r') as fin:
            res = renderer.get_ast(token.Document(fin))
        exp_res = {'children': [{'children': [{'content': 'Simple', 'type': 'RawText'}],
                                 'level': 1,
                                 'type': 'Heading'},
                                {'children': [{'content': 'echo foo\necho bar\n',
                                               'type': 'RawText'}],
                                 'language': 'shell',
                                 'type': 'CodeFence'}],
                   'footnotes': {},
                   'type': 'Document'}

        self.assertEqual(res, exp_res)


if __name__ == '__main__':
    unittest.main()
