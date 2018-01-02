# -*- coding: utf-8 -*-

import unittest

import mistletoe
import mistletoe.ast_renderer as renderer
import mistletoe.block_token as token


class SimDemMistletoeTestSuite(unittest.TestCase):
    """Lexer test cases."""

    def test_ast(self):
        self.maxDiff = None
        file_path = 'content/simple/README.md'
        with open(file_path, 'r') as fin:
            res = renderer.get_ast(token.Document(fin))
        exp_res = {'children': [{'children': [{'content': 'this is text', 'type': 'RawText'}],
                                    'type': 'Paragraph'},
                                {'children': [{'content': 'echo foo\necho bar\n',
                                                'type': 'RawText'}],
                                    'language': 'shell',
                                    'type': 'BlockCode'},
                                {'children': [{'content': 'more text', 'type': 'RawText'}],
                                    'type': 'Paragraph'},
                                {'children': [{'content': 'echo baz\n', 'type': 'RawText'}],
                                'language': 'shell',
                                    'type': 'BlockCode'},
                                {'children': [{'content': 'even more text', 'type': 'RawText'}],
                                    'type': 'Paragraph'}],
                    'footnotes': {},
                    'type': 'Document'}

        self.assertEqual(res, exp_res)


if __name__ == '__main__':
    unittest.main()
