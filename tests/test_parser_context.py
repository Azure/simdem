# -*- coding: utf-8 -*-
"""SimDem Test Case"""

import configparser
import unittest

from .context import context

class MistletoeParserTestSuite(unittest.TestCase):
    """Advanced test cases."""

    parser = None

    def setUp(self):
        config = configparser.ConfigParser()
        config.read("content/config/unit_test.ini")

        self.parser = context.ContextParser()

    def test_full(self):
        """Test parsing a document with all features in it"""
        file_path = 'content/complete-features/context.md'
        res = self.parser.parse_file(file_path)
        exp_res = {
            'prerequisites': ['prereq.md', 'prereq-2.md'],
            'commands': [
                {'command': 'echo foo'},
                {'command': 'echo bar'},
                {'command': 'echo baz', 'expected_result': 'baz'}],
            'next_steps': [
                {'title': 'Step #1', 'target': 'step-1.md'},
                {'title': 'Step #2', 'target': 'step-2.md'}
            ]
        }

        self.assertEqual(res, exp_res)


if __name__ == '__main__':
    unittest.main()
