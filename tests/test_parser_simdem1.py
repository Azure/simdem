# -*- coding: utf-8 -*-
"""SimDem Test Case"""

import configparser
import unittest
import pprint
from .context import simdem1

class SimDem1ParserTestSuite(unittest.TestCase):
    """Advanced test cases."""

    parser = None

    def setUp(self):
        config = configparser.ConfigParser()
        config.read("content/config/unit_test.ini")

        self.parser = simdem1.SimDem1Parser()

    def test_full(self):
        """Test parsing a document with all features in it"""
        self.maxDiff = None
        file_path = 'content/simdem1/README.md'
        res = self.parser.parse_file(file_path)

        exp_res = [{'content': 'Prerequisites', 'level': 1, 'type': 'heading'},
                    {'content': 'This is the prerequisite section.  SimDem looks for a set of '
                                'links to extract and run through first',
                    'type': 'text'},
                    {'content': ' * prereq-validation-pass', 'type': 'text'},
                    {'content': ['prereq-validaiton-pass.md'], 'type': 'prerequisite'},
                    {'content': "They don't even need to be in the same list", 'type': 'text'},
                    {'content': ' * prereq-validation-fail', 'type': 'text'},
                    {'content': ['prereq-validaiton-fail.md'], 'type': 'prerequisite'},
                    {'content': 'By this point, the prerequisites have either run or have passed '
                                'their validation',
                    'type': 'text'},
                    {'content': 'Do stuff here', 'level': 1, 'type': 'heading'},
                    {'content': 'We want to execute this because the code type is shell',
                    'type': 'text'},
                    {'content': ['echo foo', 'echo bar', 'var=foo'], 'type': 'commands'},
                    {'content': 'Validation', 'level': 1, 'type': 'heading'},
                    {'content': 'This is a validation section.  If this validation section '
                                'passes, we stop processing this file',
                    'type': 'text'},
                    {'content': 'Results:', 'type': 'text'},
                    {'content': 'Do more stuff here', 'level': 1, 'type': 'heading'},
                    {'content': ['echo baz'], 'type': 'commands'},
                    {'content': 'Results', 'level': 1, 'type': 'heading'},
                    {'content': 'The only thing that makes it a result is the code type is '
                                'result. We assume the result is for the last command of the last '
                                'code block',
                    'type': 'text'},
                    {'content': 'baz', 'type': 'result'},
                    {'content': 'Next Steps', 'level': 1, 'type': 'heading'},
                    {'content': 'The list inside this block are steps that could be followed when '
                                'performing an interactive tutorial',
                    'type': 'text'}]
        pprint.pprint(res)
        self.assertEqual(res, exp_res)


if __name__ == '__main__':
    unittest.main()
