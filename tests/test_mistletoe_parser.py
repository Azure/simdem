# -*- coding: utf-8 -*-

from .context import simdem, renderer

import unittest
import os.path
import configparser

class MistletoeParserTestSuite(unittest.TestCase):
    """Advanced test cases."""

    renderer = None

    def setUp(self):
        self.maxDiff = None
        config = configparser.ConfigParser()
        config.read("content/config/unit_test.ini")

        self.renderer = renderer.SimdemMistletoeRenderer()

    def test_full(self):
        file_path = 'content/complete-features/README.md'
        res = self.renderer.render_file(file_path)
        exp_res = {
            'prerequisites': ['prereq.md', 'prereq-2.md'],
            'commands': [
                { 'command': 'echo foo' },
                { 'command': 'echo bar' },
                { 'command': 'echo baz', 'expected_result': 'baz' } ]
        }

        self.assertEqual(res, exp_res)


if __name__ == '__main__':
    unittest.main()
