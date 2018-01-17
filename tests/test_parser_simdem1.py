# pylint: disable=C0330
"""SimDem Test Case"""

import configparser
import unittest
import pprint
from simdem.parser import simdem1

class SimDem1ParserTestSuite(unittest.TestCase):
    """Advanced test cases."""

    parser = None

    def setUp(self):
        config = configparser.ConfigParser()
        config.read("content/config/unit_test.ini")

        self.parser = simdem1.SimDem1Parser()

    def test_full(self):
        """Test parsing a document with all features in it"""
        self.maxDiff = None # pylint: disable=C0103
        file_path = 'content/simdem1/README.md'
        res = self.parser.parse_file(file_path)

        # This is pretty brittle.  It might be valuable to have a test document with less content
        exp_resl = {'body': [{'content': 'Prerequisites', 'level': 1, 'type': 'heading'},
          {'content': 'This is the prerequisite section.  SimDem looks for a '
                      'set of links to extract and run through first',
           'type': 'text'},
          {'content': "They don't even need to be in the same list",
           'type': 'text'},
          {'content': 'By this point, the prerequisites have either run or '
                      'have passed their validation',
           'type': 'text'},
          {'content': 'Did our prerequisites run?',
           'level': 1,
           'type': 'heading'},
          {'content': ['echo prereq_ignored = $prereq_ignored',
                       'echo prereq_processed = $prereq_processed'],
           'type': 'commands'},
          {'content': 'Do stuff here', 'level': 1, 'type': 'heading'},
          {'content': 'We want to execute this because the code type is shell',
           'type': 'text'},
          {'content': ['echo foo', 'var=bar'], 'type': 'commands'},
          {'content': 'Do more stuff here', 'level': 1, 'type': 'heading'},
          {'content': 'We assume the result is for the last command of the '
                      'last code block',
           'type': 'text'},
          {'content': ['echo baz', 'echo $var'],
           'expected_result': 'bar\n',
           'type': 'commands'},
          {'content': 'Next Steps', 'level': 1, 'type': 'heading'},
          {'content': 'The list inside this block are steps that could be '
                      'followed when performing an interactive tutorial',
           'type': 'text'}],
 'prerequisites': ['content/simdem1/prereq-ignored.md',
                   'content/simdem1/prereq-processed.md']}
        pprint.pprint(res)
        self.assertEqual(res, exp_resl)


if __name__ == '__main__':
    unittest.main()
