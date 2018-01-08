# -*- coding: utf-8 -*-
""" Test Codeblock Parser """

import configparser
import unittest

from .context import codeblock


class MistletoeParserTestSuite(unittest.TestCase):
    """Advanced test cases."""

    renderer = None

    def setUp(self):
        config = configparser.ConfigParser()
        config.read("content/config/unit_test.ini")

        self.renderer = codeblock.CodeBlockParser()

    def test_full(self):
        """ Test the full featureset of codeblock parser """
        file_path = 'content/complete-features/codeblock.md'
        res = self.renderer.parse_file(file_path)
        exp_res = {
            'prerequisites': ['prereq.md', 'prereq-2.md'],
            'commands': [
                {'command': 'echo foo'},
                {'command': 'echo bar'},
                {'command': 'echo baz', 'expected_result': 'baz'}],
            'next_steps': [
                {'title': 'step-1.md', 'target': 'step-1.md'},
                {'title': 'step-2.md', 'target': 'step-2.md'}
            ]
        }

        self.assertEqual(res, exp_res)


if __name__ == '__main__':
    unittest.main()
