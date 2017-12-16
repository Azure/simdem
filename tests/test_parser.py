# -*- coding: utf-8 -*-

from .context import simdem, demo

import unittest
import os.path
import configparser
import mistune

class SimDemTestSuite(unittest.TestCase):
    """Advanced test cases."""

    test_file = '/tmp/foo'
    parser = None

    def setUp(self):
        os.remove(self.test_file) if os.path.exists(self.test_file) else None
        config = configparser.ConfigParser()
        config.read("content/config/unit_test.ini")

        self.parser = simdem.Parser(mistune.BlockLexer())

    def test_parse_ref_from_text(self):
        self.assertEquals('./nested_prereq.md', self.parser.parse_ref_from_text('We should be able to run [nested prerequisites](./nested_prereq.md).'))

    def test_parse_doc2(self):
        doc = """foo
# Prerequisites

prereq.md
prereq-2.md

# Do stuff here
```shell
echo foo
echo bar
```

# Do more stuff here
```shell
echo baz
```

Results:
```result
baz
```


"""
        exp_res = {
            'prerequisites': ['prereq.md', 'prereq-2.md'],
            'commands': [
                { 'command': 'echo foo' },
                { 'command': 'echo bar' },
                { 'command': 'echo baz', 'expected_result': 'baz' } ]
        }
        res = self.parser.parse_doc2(doc)
        self.assertEquals(res, exp_res)

if __name__ == '__main__':
    unittest.main()
